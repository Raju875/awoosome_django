from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, Group
from django.contrib.auth.forms import AdminPasswordChangeForm

from django.utils.translation import ngettext as __, gettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import path, reverse

from django.shortcuts import render

from .forms import UserCreateForm, UserEditForm
from .models import CustomUser

User = get_user_model()


class CustomAdminPermissionMixin():
    """Permissions"""

    def has_permission(self, request, action):
        opts = self.opts
        code_name = f'{action}_{opts.model_name}'
        return request.user.has_perm(f'{opts.app_label}.{code_name}')

    def has_module_permission(self, request):  # just like menu accessibility
        if super().has_module_permission(request):
            return True

    def has_add_permission(self, request):
        # if request.user.has_perm('post.add_posts'):
        #     return True
        # return False
        return self.has_permission(request, 'add')

    def has_view_permission(self, request, obj=None):
        # if request.user.has_perm('post.view_posts'):
        #     return True
        # return False
        return self.has_permission(request, 'view')

    def has_change_permission(self, request, obj=None):
        # if request.user.has_perm('post.change_posts'):
        #     return True
        # return False
        return self.has_permission(request, 'change')

    def has_delete_permission(self, request, obj=None):
        # if request.user.has_perm('post.delete_posts'):
        #     return True
        # return False
        return self.has_permission(request, 'delete')


def admin_message(self, request, updated):
    self.message_user(request, __(
        '%d user updated successfully.',
        '%d users updated successfully.',
        updated,
    ) % updated, messages.SUCCESS)


@admin.action(description='Mark staff to user')
def staff_true_selected(self, request, queryset):
    updated = queryset.update(is_staff=True)
    admin_message(self, request, updated)


@admin.action(description='Mark not staff to user')
def staff_false_selected(self, request, queryset):
    updated = queryset.exclude(is_superuser=True).update(is_staff=False)
    admin_message(self, request, updated)


# class CustomUserAdmin(UserAdmin):
class CustomUserAdmin(CustomAdminPermissionMixin, admin.ModelAdmin):
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (_('Personal info'), {
    #      'fields': ('name', 'email', 'address', 'phone')}),
    #     (_('Permissions'), {
    #         'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    #     }),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    # add_fieldsets = (
    #     ('Tokyo', {
    #         'classes': ('wide',),
    #         'fields': ('username', 'password1', 'password2'),
    #     }),
    # )

    # override base fieldsets
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = (
                (None, {'fields': ('username', 'password')}),
                (_('Personal info'), {
                 'fields': ('name', 'email', 'address', 'phone')}),
                (_('Permissions'), {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                }),
                (_('Important dates'), {
                    'fields': ('last_login', 'date_joined')}),
            )
        else:
            fieldsets = (
                (None, {'fields': ('username', 'password')}),
                (_('Personal info'), {
                 'fields': ('name', 'email', 'address', 'phone')}),
                (_('Permissions'), {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                }),
                (_('Important dates'), {
                    'fields': ('last_login', 'date_joined')}),
            )
        return fieldsets


    # get & modify form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields:
            is_superuser = request.user.is_superuser
            if not is_superuser:
                form.base_fields['is_active'].disabled = True
                form.base_fields['is_staff'].disabled = True
                form.base_fields['is_superuser'].disabled = True
                form.base_fields['groups'].disabled = True
                form.base_fields['user_permissions'].disabled = True
            form.base_fields['last_login'].disabled = True
            form.base_fields['date_joined'].disabled = True
        return form

    add_form = UserCreateForm
    form = UserEditForm
    model = CustomUser 
    change_password_form = AdminPasswordChangeForm

    list_display = ('username', 'email_link', 'is_staff', 'is_active')
    list_display_links = ('username',)
    list_per_page = 10

    """custom queryset on list"""
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    show_full_result_count = False

    search_fields = ('username', 'name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    """custom action"""
    actions = [staff_true_selected, staff_false_selected]
    # admin.site.disable_action('delete_selected')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
            if 'staff_true_selected' in actions:
                del actions['staff_true_selected']
        return actions

    actions_selection_counter = True
    save_as = True
    save_as_continue = True

    # custom link, url adn view
    @admin.display(description='Email')
    def email_link(self, obj):
        return mark_safe('<a target="_blank" href="%s/%s/%s/">%s</a>' % ('/admin/post/posts', obj.id, 'email-view', obj.email))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:user_id>/email-view/',
                 self.admin_site.admin_view(self.my_view), name='post_posts_email_view'),
        ]

        return my_urls + urls

    def my_view(self, request, user_id):
        user = User.objects.get(id=user_id)
        return render(request, 'post/admin/email_view.html', {'email': user.email})


    # view_on_site link in change/view form beside history on top
    def view_on_site(self, obj):
        url = reverse('users:profile')
        return url


    # custom template
    # add_form_template = 'users/admin/add.html'
    # change_form_template = 'users/admin/change.html'

admin.site.site_header = 'Awoosome Django'
admin.site.site_title = 'Awoosome Django'
admin.site.index_title = 'Awoosome Django'

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.unregister(Group)
# admin.site.disable_action('delete_selected')
