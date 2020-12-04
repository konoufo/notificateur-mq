import json

from django.core.serializers.json import DjangoJSONEncoder

from .BaseNotification import BaseNotification


class NotificationCalcul(BaseNotification):
    """Permet de créer une notification de changement du statut d'un calcul en cours
    et l'envoyer aux observateurs qui écoutent sur le topic propre à la tâche ou un topic parent."""

    def __init__(self):
        self.calcul = None

    def obtenirCleRoutage(self):
        try:
            lRoutage = 'taches.projet.{calcul.projet.pk}.{calcul.pk}'.format(calcul=self.calcul)
        except AttributeError:
            lRoutage = 'taches.{calcul.pk}'.format(calcul=self.calcul)
        return lRoutage

    def obtenirMessage(self):
        lObjetMsg = self.calcul.json()
        lObjetMsg.update({'type': 'calcul'})
        return json.dumps(lObjetMsg, cls=DjangoJSONEncoder)

    @classmethod
    def creerNotification(cls, *args, **kwargs):
        # Est un alias pour la méthode `creerNotificationStatut`. Permet de
        # respecter l'interface de BaseNotification
        cls.creerNotificationStatut(*args, **kwargs)

    @classmethod
    def creerNotificationStatut(cls, pCalcul):
        # crée et retourne un objet NotificationCalcul
        assert pCalcul.statut
        lNotification = cls()
        lNotification.calcul = pCalcul
        return lNotification
