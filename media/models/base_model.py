from django.db import models


class SafeDeleteQueryset(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True)
        for item in self:
            item.save()


class FilterDeletedManager(models.Manager):
    def get_queryset(self):
        q = SafeDeleteQueryset(self.model, using=self._db)
        return q.filter(is_deleted=False)


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    objects = FilterDeletedManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
