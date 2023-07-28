from enum import Enum
from typing import List, Optional
class Sex(Enum):
    """
    Enumeration class representing the sex of a person
    """
    Male = 'm'
    Female = 'f'

class Person:
    """
       Class representing a person with a name and sex.

       Attributes:
           name (str): The name of the person.
           sex (Sex): The sex of the person, can be either Male or Female.
           mother (Optional[Person]): Reference to the mother of the person, can be None.
           father (Optional[Person]): Reference to the father of the person, can be None.
    """
    def __init__(self, name: str, sex: Sex):
        self.name: str = name
        self.sex: Sex = sex
        self.mother: Optional[Person] = None
        self.father: Optional[Person] = None

def cousin_grade(person1: Person, person2: Person) -> int:
    """
       Calculates the cousin grade between two persons.

       The cousin grade represents how many generations apart the two individuals have a common ancestor.
       If the two persons have no common ancestors, the cousin grade will be -1.

       Args:
           person1 (Person): The first person.
           person2 (Person): The second person.

       Returns:
           int: The cousin grade between the two persons.
    """
    def get_ascendants(person: Person) -> set:
        ascendants = set()
        current_person = person
        while current_person:
            father = current_person.father
            mother = current_person.mother
            if father:
                ascendants.add(father)
                ascendants.update(get_ascendants(father))
            if mother:
                ascendants.add(mother)
                ascendants.update(get_ascendants(mother))
            current_person = None if (not father and not mother) else father or mother

        return ascendants

    ascendants1 = get_ascendants(person1)
    ascendants2 = get_ascendants(person2)

    common_ascendants = ascendants1 & ascendants2
    if len(common_ascendants) == 0:
        return -1

    grade = 0
    while common_ascendants:
        grade += 1
        new_common_ascendants = set()
        for ascendant in common_ascendants:
            if ascendant.father:
                new_common_ascendants.add(ascendant.father)
            if ascendant.mother:
                new_common_ascendants.add(ascendant.mother)

        common_ascendants = new_common_ascendants

    return grade
class Adult(Person):
    """
     Subclass of Person representing an adult with a job, marriage status, and children.

     Attributes:
        name (str): The name of the adult.
        sex (Sex): The sex of the adult, can be either Male or Female.
        job (str): The job of the adult.
        married_to (Optional[Person]): Reference to the adult is married to, can be None if not married.
        children_list (List[Child]): List of children the adult has.
    """
    def __init__(self, nume: str, sex: Sex, job: str):
        super().__init__(nume, sex)
        self.job: str = job
        self.married_to: Optional[Person] = None
        self.children_list: List[Child] = []

    def description(self) -> str:
        """
            Returns a string with information about the adult, including name, sex, job, children, and marital status.

            Returns:
                str: A formatted string with information about the adult.
         """
        children = ', '.join([child.name for child in self.children_list]) if self.children_list else 'None'
        married_to = self.married_to.name if self.married_to else 'No one'
        return f'Nume: {self.name}, Sex: {self.sex.value}, Job: {self.job}, Children: {children}, Married to: {married_to}'

    def have_child_with(self, other_person, child_name: str, sex_child: Sex, school: str) -> 'Child':
        """
            Creates a child between two adults and returns the child.

            Args:
                other_person (Adult): The other adult with whom to have the child.
                child_name (str): The name of the child.
                sex_child (Sex): The sex of the child, can be either Male or Female.
                school (str): The school the child will attend.

            Returns:
                Child: The newly created child object.

            Raises:
                ValueError: If both adults have the same sex or if either adult is already married.
        """
        if self.sex == other_person.sex:
            raise ValueError('Reproduction is not possible between two people of the same sex')

        child = Child(child_name, sex_child, school, self, other_person)
        self.children_list.append(child)
        other_person.children_list.append(child)

        return child

    def marriage(self, other_person) -> None:
        """
        Performs a marriage between two adults.

        Args:
            other_person (Adult): The other adult to marry.

         Raises:
            ValueError: If either adult is already married or if both adults have the same sex.
        """
        if self.married_to is not None or other_person.married_to is not None:
            raise ValueError("Both adults must be divorced to get married")

        if self.sex == other_person.sex:
            raise ValueError("The marriage between two people with the same sex is not possible")

        self.married_to = other_person
        other_person.married_to = self

    def divorce(self, other_person) -> None:
        """
        Divorces two married adults.

        Args:
            other_person (Adult): The other adult to divorce.

        Raises:
            ValueError: If the two adults are not married to each other.
        """
        if self.married_to is not None and self.married_to == other_person:
            self.married_to = None
            other_person.married_to = None

class Child(Person):
    """
    Subclass of Person representing a child with a school, mother, and father.

    Attributes:
        name (str): The name of the child.
        sex (Sex): The sex of the child, can be either Male or Female.
        school (str): The school the child attends.
        father (Adult): Reference to the father of the child.
        mother (Adult): Reference to the mother of the child.
    """
    def __init__(self, nume: str, sex: Sex, school: str, mother: Adult, father: Adult):
        super().__init__(nume, sex)
        self.school: str = school
        self.father: Adult = father
        self.mother: Adult = mother

    def description(self) -> str:
        """
        Returns a string with information about the child, including name, sex, school, mother, and father.

        Returns:
            str: A formatted string with information about the child.
        """
        return f'Nume: {self.name}, Sex:{self.sex.value}, School: {self.school}, Mother: {self.mother.name}, Father: {self.father.name}'

    def become_adult(self, job: str) -> 'Adult':
        """
        Transitions the child into an adult with a given job.

        Args:
            job (str): The job of the adult.

        Returns:
            Adult: The newly created adult object.

        Note:
            This method updates the child's school attribute to None.
        """
        adult = Adult(self.name, self.sex, job)
        index_in_mother = self.mother.children_list.index(self)
        index_in_father = self.father.children_list.index(self)

        self.mother.children_list[index_in_mother] = adult
        self.father.children_list[index_in_father] = adult

        self.school = None

        return adult

adult1 = Adult('Ion', Sex.Male, 'engineer')
adult2 = Adult('Elena', Sex.Female, 'doctor')
adult3 = Adult('Bogdan', Sex.Male, 'lawyer')
adult4 = Adult('Ana', Sex.Female, 'teacher')

adult1.marriage(adult2)
adult2.divorce(adult1)
adult2.marriage(adult3)

child1 = adult2.have_child_with(adult1, 'Alex', Sex.Male, 'Primary School')
child2 = adult4.have_child_with(adult1, 'Ioana', Sex.Female, 'High school ')

child3 = adult2.have_child_with(adult1, 'Alexandra', Sex.Female, 'Primary School')
child4 = adult2.have_child_with(adult3, 'Ionel', Sex.Male, 'High school')

print('Information about adults: ')
print(adult1.description())
print(adult2.description())
print(adult3.description())
print(adult4.description())

print('\nInformation about children: ')
print(child1.description())
print(child2.description())
print(child3.description())
print(child4.description())

print('\nChildren become Adults')
new_adult = child1.become_adult('dancer')
print(new_adult.description())

print('\nCousin Grade: ')

parent1 = Person('Vasile', Sex.Male)
parent2 = Person('Maria', Sex.Female)
parent3 = Person('Gheorghe', Sex.Male)
parent4 = Person('Mihaela', Sex.Female)
parent5 = Person('Ioan', Sex.Male)

adult1.mother = parent2
adult1.father = parent1
adult2.mother = parent3
adult2.father = parent4

parent1.father = parent5
parent4.father = parent5

print(f'The degree of {adult1.name} and {adult2.name}: {cousin_grade(adult1, adult2)}')

