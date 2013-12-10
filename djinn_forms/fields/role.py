from pgauth.models import Role
from djinn_forms.widgets.relate import RelateWidget
from djinn_contenttypes.utils import object_to_urn
from relate import RelateField, RelateSingleField, UpdateRelations, \
    UpdateRelation


def _profile_to_user_or_group(profile):

    return getattr(profile, "user", getattr(profile, "usergroup", None))


class UpdateRoles(UpdateRelations):

    def __init__(self, instance, data, role):
        self.instance = instance
        self.rms = data.get('rm', [])
        self.adds = data.get('add', [])
        self.role = role

    def update(self):

        # Unrelate
        for profile in self.rms:
            self.instance.rm_local_role(self.role, 
                                        _profile_to_user_or_group(profile))

        # Relate
        for profile in self.adds:
            self.instance.add_local_role(self.role,
                                         _profile_to_user_or_group(profile))


class UpdateRole(UpdateRelation):

    def __init__(self, instance, data, role):
        self.instance = instance
        self.tgt = data
        self.role = role

    def update(self):

        if self.tgt:
            self.instance.rm_local_role(self.role)
            self.instance.add_local_role(self.role,
                                         _profile_to_user_or_group(self.tgt))


class LocalRoleField(RelateField):

    """ Field for assigning roles to users or groups on a given object """

    updater = UpdateRoles

    def __init__(self, role_id, content_types, *args, **kwargs):

        self.role = Role.objects.get(name=role_id)

        super(LocalRoleField, self).__init__(self.role, content_types, *args,
                                        **kwargs)

    def prepare_value(self, data):

        """ Get the existing local roles for the given role.  If
        data['rm'] has values, filter those out of the result.  If
        data['add'] has values, add those to the result
        """

        roles = self.instance.get_local_roles(role_filter=[self.role.name])

        users_or_groups = [(lrole.user or lrole.usergroup)
                           for lrole in roles
                           if lrole.user or lrole.usergroup]

        users_or_groups = [u.profile for u in users_or_groups]

        try:
            users_or_groups = filter(lambda x: x not in data['rm'],
                                     users_or_groups)
        except:
            pass

        try:
            users_or_groups += data['add']
        except:
            pass

        return [{'label': unicode(profile),
                 'value': object_to_urn(profile)} for profile in
                users_or_groups]


class LocalRoleSingleField(LocalRoleField):

    updater = UpdateRole

    def prepare_value(self, data):

        """ Get existing role, if it's there """

        value = super(LocalRoleSingleField, self).prepare_value(data)

        if value:
            return value[0]
        else:
            return None