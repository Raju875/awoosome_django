from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.utils.safestring import mark_safe
from django.urls import path
from django.shortcuts import render

from .models import Posts, User

class CustomAdminPermissionMixin():
    """Permissions"""
    def has_permission(self, request, action):
        opts = self.opts
        code_name = f'{action}_{opts.model_name}'
        return request.user.has_perm(f'{opts.app_label}.{code_name}')

    def has_module_permission(self, request): # just like menu accessibility
        return True
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
    self.message_user(request, ngettext(
        '%d row updated successfully.',
        '%d rows updated successfully.',
        updated,
    ) % updated, messages.SUCCESS)


@admin.action(description='Mark as active')
def active_selected(self, request, queryset):
    updated = queryset.exclude(is_active=True).update(is_active=True)
    admin_message(self, request, updated)


@admin.action(description='Mark as inactive')
def inactive_selected(self, request, queryset):
    updated = queryset.exclude(is_active=False).update(is_active=False)
    admin_message(self, request, updated)


# custom admin filter
class PhoneListFilter(admin.SimpleListFilter):
    title = _('Phone filter')

    parameter_name = 'phone'

    def lookups(self, request, model_admin):
        return (
            ('has_phone', _('has phone')),
            ('no_phone', _('no phone')),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'has_phone':
            return queryset.exclude(phone__isnull=True)
        if self.value().lower() == 'no_phone':
            return queryset.filter(phone__isnull=True)
            

# --- Model Register in Admin
@admin.register(Posts)
class PostAdmin(CustomAdminPermissionMixin, admin.ModelAdmin):
    """list/table"""
    list_display = ("__str__", "camel_case_name", "email_link", "phone", "image_tag", "is_active",)
    list_display_links = ('camel_case_name', 'image_tag')
    list_editable = ("phone", "is_active")
    search_fields = ["name", "email"]
    list_per_page = 25

    """custom finction on list"""
    @admin.display(description='Name')
    def camel_case_name(self, obj):
        return ("%s" % (obj.name)).title()

    """custom queryset on list"""
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    """search/filter"""
    list_filter = ('is_active', PhoneListFilter)
    
    """custom action"""
    actions = [active_selected, inactive_selected]
    # admin.site.disable_action('delete_selected')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
            if 'inactive_selected' in actions:
                del actions['inactive_selected']
        return actions

    show_full_result_count = True


    """add/edit/view form"""
    # fieldsets = (
    #     ('Contact Info', {'fields': (('name', 'email'), 'phone', 'photo', 'user',)}),
    #     ('Message', {'fields': ('message',)}),
    #     ('Advanced options', {
    #         'classes': ('collapse',),
    #         'fields': ('is_active', 'created_by', 'updated_by'),
    #     }),
    # )
    # fields = (('name', 'email'), 'message')

    # override base fieldsets
    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (
                ('Contact Info', {
                 'fields': (('name', 'email'), 'phone', 'photo', 'user',)}),
                ('Message', {'fields': ('message',)}),
                ('Advanced options', {
                    'classes': ('collapse',),
                    'fields': ('is_active',)
                }),
            )
        else:
            return (
                ('Contact Info', {
                 'fields': (('name', 'email'), 'phone', 'photo', 'user',)}),
                ('Message', {'fields': ('message',)}),
                ('Advanced options', {
                    'classes': ('collapse',),
                    'fields': ('is_active', 'created_by', 'updated_by')
                }),
            )

    # get & modify form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields:
            is_superuser = request.user.is_superuser
            if not is_superuser:
                if not request.user.has_perm('post.change_post_status'):
                    form.base_fields['is_active'].disabled = True
                form.base_fields["user"].queryset = User.objects.filter(id=request.user.id)
        return form

    # get readonly fields
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
           return []
        else:
            return ['created_by', 'updated_by']

    # custom link dispaly
    @admin.display(description='Email')
    def email_link(self, obj):
        return mark_safe('<a target="_blank" href="%s/%s/%s/">%s</a>' % ('/admin/post/posts', obj.user.id, 'email-view', obj.user.email))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:user_id>/email-view/', self.admin_site.admin_view(self.my_view), name='post_posts_email_view'),
        ]
        return my_urls + urls

    def my_view(self, request, user_id):
        user = User.objects.get(id=user_id)
        return render(request, 'post/admin/email_view.html', {'email': user.email})


    """save functionality"""
    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    """Other methods"""
    # change_list_template = 'admin/post/post_filter_list.html'


