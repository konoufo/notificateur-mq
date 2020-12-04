from abc import ABCMeta, abstractmethod, abstractclassmethod

from django.conf import settings
import pika


MESSAGE_METHODE_ABSTRAITE = 'Cette fonctionnalité doit être implémentée par une classe concrète.'


class BaseNotification(metaclass=ABCMeta):
    # FIXME: utiliser les callbacks de pika pour logger les erreurs de connexion
    def envoyer(self):
        host, virtual_host = settings.MQ_HOST, settings.MQ_VIRTUAL_HOST
        credentials = pika.credentials.PlainCredentials(settings.MQ_NOTIFICATEUR_ID, settings.MQ_NOTIFICATEUR_SECRET)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host,
                                      port=settings.MQ_PORT,
                                      virtual_host=virtual_host,
                                      credentials=credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange='amq.topic', exchange_type='topic', durable=True)
        channel.basic_publish(exchange='amq.topic', routing_key=self.obtenirCleRoutage(), body=self.obtenirMessage())
        connection.close()

    @abstractmethod
    def obtenirCleRoutage(self):
        raise NotImplementedError(MESSAGE_METHODE_ABSTRAITE)

    @abstractmethod
    def obtenirMessage(self):
        raise NotImplementedError(MESSAGE_METHODE_ABSTRAITE)

    @abstractclassmethod
    def creerNotification(cls, *args, **kwargs):
        """ Crée une notification et renseigne les attributs de l'objet avec des informations
        nécessaires à la construction du message et de la clé de routage.
        """
        raise NotImplementedError(MESSAGE_METHODE_ABSTRAITE)
