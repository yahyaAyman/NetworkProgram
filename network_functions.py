'''CSC108 Assignment 3: Social Networks'''

from typing import List, Tuple, Dict, TextIO


def load_profiles(profiles_file: TextIO, person_to_friends: Dict[str, List[str]], \
                  person_to_networks: Dict[str, List[str]]) -> None:
    '''Update the person_to_friends dictionary and the person_to_networks
    dictionary to include data from profiles_file.

    Docstring examples not given since the result depends on input data.
    '''
    file = profiles_file.readlines()
    if file is not None:
        for i in range(len(file)):
            file[i] = file[i].rstrip('\n')
        person_name = file[0].split(", ")[1] + ' ' + \
        file[0].split(", ")[0]
        person_to_friend_dict = {}
        person_to_network_dict = {}
        new_dict(file, person_to_friend_dict,\
                         person_to_network_dict, person_name)
        new_old_friend(person_to_friends, person_to_friend_dict)
        update_old_networks(person_to_networks, person_to_network_dict)

def new_dict(file: TextIO, person_to_friend_dict,\
                     person_to_network_dict, person_name):
    """
    A new dictinary is created using the dat from the file. Storing the data
    in the relevant dictionary
    """
    person_to_friend_dict[person_name] = []
    iterator = 1
    while iterator < len(file):
        if iterator < len(file) - 1:
            if file[iterator] == '':
                splitting_name = file[iterator+1].split(", ")
                person_name = splitting_name[1] + " " + splitting_name[0]
                if person_name not in person_to_friend_dict:
                    person_to_friend_dict[person_name] = []
                iterator += 1
            elif "," in file[iterator]:
                current_friend = file[iterator].split(", ")
                person_to_friend_dict[person_name].append(current_friend[1] \
                                   + " " + current_friend[0])
            else:
                if person_to_network_dict.get(person_name) is None:
                    person_to_network_dict[person_name] = []
                person_to_network_dict[person_name].append(file[iterator])
        iterator += 1


def new_old_friend(person_to_friends: Dict[str, List[str]],\
                   person_to_friend_dict: Dict[str, List[str]]):
    '''
    Updates the person to friends dictionary with the values from the person
    to friend dictionary
    '''
    for key in person_to_friend_dict:
        if key in person_to_friends:
            current_list = person_to_friends.get(key)
            new_list = person_to_friend_dict.get(key)
            larger_num = len(new_list)
            if len(current_list) > len(new_list):
                larger_num = len(current_list)
            elif len(new_list) < len(current_list):
                larger_num = len(new_list)
            for num in range(larger_num):
                if num < len(new_list) and new_list[num] in current_list:
                    del new_list[num]
            final_list = new_list + current_list
            person_to_friends[key] = final_list
        else:
            person_to_friends.update({key:person_to_friend_dict[key]})

def update_old_networks(person_to_networks: Dict[str, List[str]],\
                        person_to_network_dict: Dict[str, List[str]]):
    """
    updates the old person to networks dictionary using the value from
    person to network dictionary
    """
    for key in person_to_network_dict:
        if key in person_to_networks:
            current_list = person_to_networks.get(key)
            new_list = person_to_network_dict.get(key)
            if len(current_list) > len(new_list):
                larger_num = len(current_list)
            elif len(new_list) < len(current_list):
                larger_num = len(new_list)
            else:
                larger_num = len(new_list)
            for num in range(larger_num):
                if new_list[num] in current_list:
                    del new_list[num]
            final_list = new_list + current_list
            person_to_networks[key] = final_list
        else:
            person_to_networks.update({key:person_to_network_dict[key]})

def get_average_friend_count(person_to_friends: Dict[str, List[str]]) -> float:
    '''
    Calculates the avarage number of friends across everyone in the person to
    friends dictionary have.

    >>> get_average_friend_count({'Jay Pritchett': ['Ayman Elsayed', 'Dara Essawi'],\
    'Dara Essawi': ['Ayman Elsayed', 'Jay Pritchett']})
    2.0
    >>> get_average_friend_count({'Jay Pritchett': ['Claire Dunphy', 'Samuel S-Sami'],\
                 'Yahya Ayman': ['Claire Dunphy', 'Sami Sami', 'Faisal Ameen']})
    2.5
    >>> get_average_friend_count({'Jay Pritchett': ['Ayman Elsayed', 'Dara Essawi'],\
                 'Dara Essawi': ['Ayman Elsayed', 'Jay Pritchett'],\
                 'David Suzuki': ['Jay Pritchett']})
    1.6666666666666667
    '''
    value_accumulator = 0

    key_accumulator = 0

    for key in person_to_friends:
        key_accumulator += 1
        value_accumulator += len(person_to_friends[key])
    if key_accumulator == 0:
        return 0.0
    else:
        avg_num_friends = value_accumulator / key_accumulator
        return avg_num_friends

def get_families(person_to_friends: Dict[str, List[str]]) -> Dict[str, List[str]]:
    '''
    Creates a new dictionary that has the last name as a key and the family members
    as values in the dictionary.

    >>> get_families({'Jay D-Money': ['Haley Gwendolyn Dunphy'],\
    'Dylan D-Money': ['Sam Pritchett']})
    {'D-Money': ['Dylan', 'Jay'], 'Dunphy': ['Haley Gwendolyn'], 'Pritchett': ['Sam']}
    >>> get_families({'Jay D-Money': ['Haley Gwendolyn Dunphy'],\
    'Dylan D-Money': ['Haley Gwendolyn Dunphy']})
    {'D-Money': ['Dylan', 'Jay'], 'Dunphy': ['Haley Gwendolyn']}
    >>> get_families({'Jay Pritchett': ['Haley Gwendolyn Dunphy'],\
    'Elissa Dunphy': ['Sam Pritchett']})
    {'Pritchett': ['Jay', 'Sam'], 'Dunphy': ['Elissa', 'Haley Gwendolyn']}
    >>> get_families({'Jay D-Money': ['Haley Gwendolyn Dunphy'],\
    'Dylan D-Money': ['Haley Gwendolyn Dunphy']})
    {'D-Money': ['Dylan', 'Jay'], 'Dunphy': ['Haley Gwendolyn']}
    '''
    names = []

    last_name_dict = {}

    names.extend(list(person_to_friends))

    for name_list in person_to_friends.values():
        names += name_list

    for name in names:
        first_name, last_name = name.rsplit(' ', 1)
        if last_name in last_name_dict:
            if first_name not in last_name_dict[last_name]:
                last_name_dict[last_name].append(first_name)
        else:
            last_name_dict[last_name] = [first_name]
    for first_name_list in last_name_dict.values():
        first_name_list.sort()

    return last_name_dict

def invert_network(person_to_networks: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Return a "network to people" dictionary based on the given 'person to networks'
    dictionary. The values in the dictionary are sorted alphabetically.

    >>> invert_network({'Mitchell Pritchett': ['Law Association']})
    {'Law Association': ['Mitchell Pritchett']}
    >>> invert_network({'Gloria Pritchett': ['Parent Teacher Association'],'Mitchell Pritchett': ['Law Association']})
    {'Parent Teacher Association': ['Gloria Pritchett'], 'Law Association': ['Mitchell Pritchett']}
    >>> invert_network({'Claire Dunphy': ['Parent Teacher Association']})
    {'Parent Teacher Association': ['Claire Dunphy']}
    """
    updated_list = []


    for key in person_to_networks:s
        for sub_key in range(len(person_to_networks[key])):
            network = person_to_networks[key][sub_key]
            if network not in updated_list:
                updated_list.append(network)

    network_of_people = {}

    recent_name_list = []

    for sub_key in range(len(updated_list)):
        for key in person_to_networks:
            if updated_list[sub_key] in person_to_networks[key]:
                if key not in recent_name_list:
                    recent_name_list.append(key)
        network_of_people.update({updated_list[sub_key]:recent_name_list})
        recent_name_list = []

    for names in recent_name_list:
        recent_name_list.sort()
    return network_of_people


def get_friends_of_friends(person_to_friends: Dict[str, List[str]], \
                           person: str) -> List[str]:
    '''
    >>> param = {'Jay Pritchett': ['Claire Dunphy', 'Gloria Pritchett',\
                'Manny Delgado'], 'Claire Dunphy': ['Jay Pritchett',\
                'Mitchell Pritchett']}
    >>> get_friends_of_friends(param , 'Jay Pritchett')
    ['Mitchell Pritchett']
    ['Cameron Tucker', 'Gloria Pritchett', 'Luke Dunphy', 'Manny Delgado', 'Mitchell Pritchett', 'Phil Dunphy']
    >>> param = {'Jay Pritchett': ['Claire Dunphy', 'Gloria Pritchett',\
                'Manny Delgado'], 'Claire Dunphy': ['Claire Dunphy',\
                'Jay Pritchett', 'Mitchell Pritchett', 'Phil Dunphy']}
    >>> get_friends_of_friends(param, 'Claire Dunphy')
    ['Gloria Pritchett', 'Jay Pritchett', 'Manny Delgado', 'Mitchell Pritchett', 'Phil Dunphy']
    >>> param = {'Claire Dunphy': ['Claire Dunphy', 'Jay Pritchett','Mitchell Pritchett',\
    'Yahya Salamh', 'Phil Dunphy']}
    >>> get_friends_of_friends(param, 'Claire Dunphy')
    ['Jay Pritchett', 'Mitchell Pritchett', 'Phil Dunphy', 'Yahya Salamh']
    >>> param = {'Jay Pritchett': ['Claire Dunphy', 'Gloria Pritchett',\
                'Manny Delgado'], 'Claire Dunphy': ['Jay Pritchett',\
                'Mitchell Pritchett', 'Phil Dunphy'],'Manny Delgado':
                ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy']}
    >>> get_friends_of_friends(param, 'Jay Pritchett')
    ['Gloria Pritchett', 'Luke Dunphy', 'Mitchell Pritchett', 'Phil Dunphy']
    '''
    connected_friends = []

    friends = person_to_friends[person]

    for friend in range(len(friends)):
        name = friends[friend]
        if name in person_to_friends:
            for names in range(len(person_to_friends[name])):
                if person_to_friends[name][names] != person:
                    connected_friends.append(person_to_friends[name][names])
                    connected_friends.sort()
    return connected_friends


def make_recommendations(person: str,\
                         person_to_friends: Dict[str, List[str]],\
                         person_to_networks: Dict[str, List[str]]) \
                         -> List[Tuple[str, int]]:

    """
    Recommends other users to the person based on the number of mutual friends from the
    users network
    >>> z = {'Claire Dunphy': ['Parent Teacher Association'],\
    'Manny Delgado': ['Chess Club'], 'Mitchell Pritchett': ['Law Association'],\
    'Alex Dunphy': ['Chess Club', 'Orchestra'],\
    'Cameron Tucker': ['Clown School', 'Wizard of Oz Fan Club'],\
    'Phil Dunphy': ['Real Estate Association'],\
    'Gloria Pritchett': ['Parent Teacher Association']}
    >>> x = {'Jay Pritchett': ['Claire Dunphy', 'Gloria Pritchett', 'Manny Delgado'],\
    'Claire Dunphy': ['Jay Pritchett', 'Mitchell Pritchett', 'Phil Dunphy'],\
    'Manny Delgado': ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'],\
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Gloria Pritchett', 'Mitchell Pritchett'],\
    'Haley Gwendolyn Dunphy': ['Dylan D-Money', 'Gilbert D-Cat'],\
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'],\
    'Dylan D-Money': ['Chairman D-Cat', 'Haley Gwendolyn Dunphy'],\
    'Gloria Pritchett': ['Cameron Tucker', 'Jay Pritchett', 'Manny Delgado'],\
    'Luke Dunphy': ['Alex Dunphy', 'Manny Delgado', 'Mitchell Pritchett', 'Phil Dunphy']}
    >>> make_recommendations("Jay Pritchett",x,z)
    [('Gloria Pritchett', 2), ('Cameron Tucker', 1),\
    ('Luke Dunphy', 1), ('Manny Delgado', 1), ('Phil Dunphy', 1)]
    >>> make_recommendations('Dylan D-Money',x,z)
    []
    >>> make_recommendations('Gloria Pritchett',x,z)
    [('Claire Dunphy', 2), ('Jay Pritchett', 2), ('Luke Dunphy', 1), ('Manny Delgado', 1)]
    """
    # I used the bubble sort method that was used during lecture and PCRS. Some of which we
    # were showed during lecture videos.

    person_network = person_to_networks.get(person)
    person_friends = person_to_friends.get(person)
    person_name = person.split(" ")
    reccomendations = []
    person_last_name = person_name[len(person_name)-1]
    for key in person_to_friends:
        current_friends = person_to_friends.get(key)
        current_network = person_to_networks.get(key)
        current_score = 0
        if person_network != None and current_network != None:
            for network in person_network:
                if network in current_network:
                    current_score += 1

        if person_friends != None:

            for friend in person_friends:
                if friend in current_friends:
                    current_score += 1

        current_name = key.split(" ")
        current_last_name = current_name[len(current_name)-1]

        if current_score > 0:
            if current_last_name == person_last_name:
                current_score += 1

        if current_score > 0 and person != key:
            reccomendations.append([key, current_score])

    reccomendations = [(-score, name) for name, score in reccomendations]
    reccomendations.sort()
    reccomendations = [(name, -score) for score, name in reccomendations]
    return reccomendations



def is_network_connected(person_to_friends: Dict[str, List[str]]) -> bool:
    '''
    Checks if there is a path that maps from one person to another in a
    dictionary forming a closed circle of friends.
    '''
    # Tried to use an algorithim my function, however it only passes some
    # cases not all from what I tested
    checked = []
    to_chec = [[begin]]
    if begin == end:
        return True

    while to_chec:
        path = to_chec.pop(0)
        node = path[-1]
        if node not in checked:
            names = graph[node]
            for name in names:
                new_path = list(path)
                new_path.append(name)
                queue.append(new_path)

            checked.append(node)
    return False




if __name__ == '__main__':
    import doctest
    doctest.testmod()
