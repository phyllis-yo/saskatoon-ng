from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from member.models import (Actor, Neighborhood, AuthUser, Person,
                           Organization, City, State, Country)
from harvest.models import (Harvest, Property, Equipment, EquipmentType,
                            RequestForParticipation, TreeType)


class RequestForParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestForParticipation
        fields = '__all__'


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    neighborhood = NeighborhoodSerializer(many=False, read_only=True)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['actor_id', 'roles', 'name', 'email', 'phone', 'neighborhood',
                  'harvests_as_pickleader', 'harvests_as_volunteer_succeeded',
                  'harvests_as_volunteer_accepted', 'harvests_as_volunteer_rejected',
                  'harvests_as_volunteer_pending', 'harvests_as_volunteer_cancelled',
                  'harvests_as_owner', 'organizations_as_contact', 'properties', 'comments']

    def get_roles(self, person):
        if hasattr(person, 'auth_user'):
            return [str(role) for role in person.auth_user.roles]
        return ""


class EquipmentTypeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = EquipmentType
        fields = ['name', 'name_fr', 'name_en']

    def get_name(self, type):
        return type.name_fr


class EquipmentSerializer(serializers.ModelSerializer):
    type = EquipmentTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Equipment
        fields = ['type', 'count']


class OrganizationSerializer(serializers.ModelSerializer):
    contact_person = PersonSerializer(many=False, read_only=True)
    neighborhood = NeighborhoodSerializer(many=False, read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)
    inventory = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['actor_id', 'civil_name', 'contact_person',
                  'phone', 'short_address', 'address', 'neighborhood',
                  'is_beneficiary', 'beneficiary_description',
                  'is_equipment_point', 'equipment_description',
                  'description', 'equipment', 'inventory']

    def get_inventory(self, org):
        return dict([
            (lang, "&;".join([e.inventory(lang) for e in org.equipment.all()]))
            for lang in ['fr', 'en']
        ])


class ActorSerializer(serializers.ModelSerializer):
    person = PersonSerializer(source='get_person', many=False, read_only=True)
    organization = OrganizationSerializer(source='get_organization', many=False, read_only=True)

    class Meta:
        model = Actor
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class TreeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeType
        fields = '__all__'


class PersonOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['pk', 'name', 'email', 'phone', 'language', 'comments',
                  'neighborhood', 'city', 'state', 'country']

    language = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_language(self, obj):
        return obj.language.name if obj.language else None

    def get_comments(self, obj):
        return obj.person.comments


class OrganizationOwnerSerializer(PersonOwnerSerializer):
    class Meta(PersonOwnerSerializer.Meta):
        model = Organization

    def get_comments(self, obj):
        return _("Owner is an Organization")


class OwnerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['is_person', 'is_organization']


class PropertyHarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = ['id', 'status', 'start_date', 'pick_leader']

    pick_leader = serializers.SerializerMethodField()

    def get_pick_leader(self, harvest):
        if harvest.pick_leader:
            return PersonSerializer(harvest.pick_leader.person).data
        return None


class PropertySerializer(serializers.ModelSerializer):
    neighborhood = NeighborhoodSerializer(many=False, read_only=True)
    city = CitySerializer(many=False, read_only=True)
    state = StateSerializer(many=False, read_only=True)
    country = CountrySerializer(many=False, read_only=True)
    title = serializers.ReadOnlyField(source="__str__")
    harvests = PropertyHarvestSerializer(many=True, read_only=True)
    last_succeeded_harvest_date = serializers.ReadOnlyField()
    address = serializers.ReadOnlyField(source="short_address")
    trees = TreeTypeSerializer(many=True, read_only=True)
    owner = serializers.SerializerMethodField()
    pending_contact_name = serializers.ReadOnlyField()
    owner_type = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'

    def get_owner(self, obj):
        if obj.owner:
            if obj.owner.is_person:
                return PersonOwnerSerializer(obj.owner.person).data
            elif obj.owner.is_organization:
                return OrganizationOwnerSerializer(obj.owner.organization).data
        return None

    def get_owner_type(self, obj):
        return OwnerTypeSerializer(obj.owner).data


class PropertyListHarvestSerializer(PropertyHarvestSerializer):
    start_date = serializers.DateTimeField(source='get_local_start', format="%Y-%m-%d")
    pick_leader = serializers.StringRelatedField(many=False)


class PropertyTreeTypeSerializer(TreeTypeSerializer):
    class Meta(TreeTypeSerializer.Meta):
        fields = ['name', 'fruit_name']


class PropertyListSerializer(PropertySerializer):
    neighborhood = serializers.StringRelatedField(many=False)
    trees = PropertyTreeTypeSerializer(many=True, read_only=True)
    harvests = PropertyListHarvestSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'neighborhood',
            'trees',
            'last_succeeded_harvest_date',
            'is_active',
            'authorized',
            'pending',
            'harvests'
        ]


class EquipmentPropertySerializer(PropertyListSerializer):
    class Meta(PropertyListSerializer.Meta):
        fields = [
            'id',
            'title',
            'neighborhood',
            'owner'
        ]


class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    property = EquipmentPropertySerializer(many=False, read_only=True)
    type = EquipmentTypeSerializer(many=False, read_only=True)
    owner = ActorSerializer(many=False, read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'


class PickLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['id', 'name']


class HarvestSerializer(serializers.ModelSerializer):
    # three different ways of getting a multimodel serializer:
    # 1) calling a model method
    pickers = serializers.ReadOnlyField(source='get_pickers')
    total_distribution = serializers.ReadOnlyField(source='get_total_distribution')
    is_open_to_requests = serializers.ReadOnlyField()
    # status_l10n = serializers.ReadOnlyField(source='get_status_l10n')
    start_date = serializers.DateTimeField(source='get_local_start', format="%Y-%m-%d")
    start_time = serializers.DateTimeField(source='get_local_start', format="%H:%M")
    end_time = serializers.DateTimeField(source='get_local_end', format="%H:%M")
    # # 2) get string rather than id from a pk
    status = serializers.StringRelatedField(many=False)
    # 3) get the full instance from another serializer class
    pick_leader = PickLeaderSerializer(many=False, read_only=True)
    trees = TreeTypeSerializer(many=True, read_only=True)
    property = PropertySerializer(many=False, read_only=True)

    class Meta:
        model = Harvest
        fields = '__all__'


class HarvestTreeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeType
        fields = ['id', 'name', 'fruit_name']


class HarvestListSerializer(HarvestSerializer):
    property = serializers.StringRelatedField(many=False)
    neighborhood = serializers.ReadOnlyField(source='get_neighborhood')
    trees = HarvestTreeTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Harvest
        fields = ['id',
                  'start_date',
                  'start_time',
                  'end_time',
                  'status',
                  'pick_leader',
                  'trees',
                  'property',
                  'neighborhood']


class CommunitySerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=False, read_only=True)
    roles = serializers.ReadOnlyField()
    role_codes = serializers.SerializerMethodField()

    class Meta:
        model = AuthUser
        fields = '__all__'

    def get_role_codes(self, instance):
        return [g.name for g in instance.role_groups]
