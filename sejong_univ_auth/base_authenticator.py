from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class AuthenticationReport:
	is_



class SejongAuthenticator(metaclass=ABCMeta):

	@abstractmethod
	def authenticate(id: str, password: str) -> bool:
		pass

