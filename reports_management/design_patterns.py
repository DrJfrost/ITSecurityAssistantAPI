#Abstract factory pattern
from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from typing import Any



#PATRON CONSTRUCTOR
class Constructor(ABC):
    
    @abstractproperty
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_a(self) -> None:
        pass

    @abstractmethod
    def produce_part_b(self) -> None:
        pass

    @abstractmethod
    def produce_part_c(self) -> None:
        pass


class AnalisisEspecifico1(Constructor):

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._product = Auditoria1()

    @property
    def product(self) -> Auditoria1:
        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        self._product.add("Auditoria1")

    def produce_part_b(self) -> None:
        self._product.add("Cita1")

    def produce_part_c(self) -> None:
        self._product.add("Reporte1")


class Auditoria1():

    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def list_parts(self) -> None:
        print(f"Product parts: {', '.join(self.parts)}", end="")


class GestorAuditoria:
   
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Constructor:
        return self._builder

    @builder.setter
    def builder(self, builder: Constructor) -> None:
        self._builder = builder


    def build_minimal_viable_product(self) -> None:
        self.builder.produce_part_a()

    def build_full_featured_product(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()

#PATRON CADENA DE RESPONSABILIDAD
class Auditoria:
    def init(self):
        self.succesor = None

    def set_succesor(self, succesor):
        self.succesor = succesor

    def handler_request(self, opt):
        pass


class AuditoriaPresencial(Auditoria):

    def handler_request(self, opt):
        if opt == 1:
            print("Face to face")
        else:
            self.succesor.handler_request(opt)

class AuditoriaVirtual(Auditoria):

    def handler_request(self, opt):
        if opt == 2:
            print("Face to Screen")
        else:
            self.succesor.handler_request(opt)


class AuditoriaDefault(Auditoria):

    def handler_request(self, opt):
        print("Opción no valida")


#PATRON INTERPRETER
class Reports:
    def init(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class ReportsNumber(Reports):

    def evaluate(self):
        return int(self.value)

class ReportsPluss(Reports):

    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()


class ReportsMinus(Reports):

    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()
