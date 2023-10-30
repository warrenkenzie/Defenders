import random

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }


defenders = {'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       },
             
             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      }
             }


monsters = {'ZOMBI': {'name': 'Zombie',
                      'maxHP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves' : 1,
                      'reward': 2
                      },

            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves' : 2,
                      'reward': 3
                      }
            }



field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]

defender_list = ['ARCHR', 'WALL']
monster_list = ['ZOMBI', 'WWOLF']

list_alphabet = ["A","B","C","D","E"]
#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field():
    #first row
    print("    1     2     3")
    #num of rows
    for row in range(5):
        print(" +-----+-----+-----+-----+-----+-----+-----+") 
        #thickness of row
        for time in range(2):
            if time == 0:
                print("{}|".format(list_alphabet[row]),end = "")
            else:
                print(" |",end = "")
            #when time = 0, print name
            #when time = 1, print attk
            #num of column
            for column in range(7):
                #position
                item = field[row][column]
                if item == None:
                    #if placeholder is None, print empty string
                    print("{:^5}|".format(""),end = "")
                else:
                    #if placeholder is not None, print content
                    #name 
                    if time == 0:
                        if (item[0] in defender_list) or (item[0] in monster_list):
                            print("{:^5}|".format(item[0]),end = "")
                    #health
                    if time == 1:
                        if (item[0] in monsters):
                            max_HP =  monsters[item[0]].get("maxHP")
                            print("{:>2}/{:<2}|".format(item[1],max_HP),end = "")
                        if (item[0] in defenders):
                            max_HP = defenders[item[0]].get("maxHP")
                            print("{:>2}/{:<2}|".format(item[1],max_HP),end = "")
                        
            print()
    print(" +-----+-----+-----+-----+-----+-----+-----+")
    return ""
        
#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    print("Turn   {}".format(game_vars.get("turn")))
    print("Threat = [{:<10}]".format(game_vars.get("threat") * "-"))  
    print("Danger Level {}".format(game_vars.get('danger_level')))
    print("Gold = {}".format(game_vars.get("gold")))
    print("Monster killed = {:d}/20".format(game_vars.get("monsters_killed")))
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):
    try:
        if not(len(position) < 3 and len(position) >0):
            print("\n" + "entered wrong input")
            return False
        char = position[0]
        row_index= (ord(char.upper())-ord("A")+1) - 1
        column_index = int(position[1]) - 1
        if (field[row_index][column_index] == None) and (column_index < 3):
            field[row_index][column_index] = [unit_name,defenders[unit_name].get("maxHP")]
        else:
            if column_index > 2:
                print("\n" + "Out Of Range")
            else:
                print("\n" + "Unable to.")
            return False
    except:
        print("ERROR")
        return False
    return True

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars):
    print("What unit do you wish to buy?")
    print("1. Archer (5 gold)\n2. Wall (3 gold)\n3. Don't buy")
    #input choice
    try:
        choice = int(input("Your choice? "))
    except:
        print("\n" + "entered wrong input")
        return True
    if choice > 3:
        print("\n" + "No option {}".format(choice))
        return True
    if choice == 1:  #Archer
        if game_vars["gold"] >= defenders['ARCHR'].get("price"):
            game_vars["gold"] -= defenders['ARCHR'].get("price")
            unit_name = defender_list[0]
            return unit_name
        else:
            print("Not enough gold")
            return True
    elif choice == 2:   #Wall
        if game_vars["gold"] >= defenders['WALL'].get("price"):
            game_vars["gold"] -= defenders['WALL'].get("price")
            unit_name = defender_list[1]
            return unit_name
        else:
            print("Not enough gold")
            return True
    elif choice == 3: #dont buy
        return True
    

#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defender_name, field, row_num, column):
    column_index = 0
    for item in field[row_num]:
        if item != None:
            #deals damage to the first monster
            if  item[0] in monster_list:
                monster_name = item[0]           
                damage_value = random.randint(defenders[defender_name].get("min_damage"), defenders[defender_name].get("max_damage"))
                item[1] -= damage_value
                if not(defender_name == "WALL"):
                    print("{} in lane {} shoots {} for {} damage!".format(defenders[defender_name].get("name"), list_alphabet[row_num],monsters[monster_name].get("name"),damage_value))
                
                #when health reaches 0 for monster
                if item[1] <= 0:
                    #monster dies
                    field[row_num][column_index] = None

                    print("{} dies!".format(monsters[monster_name].get("name")))

                    #gain gold
                    reward = monsters[monster_name].get('reward')
                    game_vars['gold'] += reward
                    game_vars['threat'] += reward
                    print("You gain {} gold as a reward.".format(reward))

                    #game_vars
                    game_vars["num_monsters"] -= 1
                    game_vars["monsters_killed"] += 1
                break;
                
        column_index += 1
    return   

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
#def monster_advance(monster_name, field, row, column):
def monster_advance(monster_name, field, row_num, column):
    #column = WHERE IM AT
    times = True
    monster = field[row_num][column]
    moves = monsters[monster_name].get("moves")
    #i + 1 is where the monster is at
    #i is what is in front of the monster
    for i in range(column-1,column- moves -1,-1):
        #if theres monster in last column
        if i == -1:
            print("A {} has reached the city! All is lost!".format(monsters[monster_name].get("name")))
            print("You have lost the game. :(")
            return True
            break;
        tile_at_which_monster_will_land = field[row_num][i]
        #first check if theres defender in front of monster
        if tile_at_which_monster_will_land != None and not(tile_at_which_monster_will_land[0] in monster_list):
            #if true theres a defender
            #deal damage
            damage_value = random.randint(monsters[monster_name].get("min_damage"), monsters[monster_name].get("max_damage"))
            tile_at_which_monster_will_land[1] -= damage_value
            if tile_at_which_monster_will_land[1] <= 0:
                field[row_num][i] = None
                field[row_num][i+1] = None
                field[row_num][i] = monster
                break;
            break;
    
        if tile_at_which_monster_will_land == None:
            field[row_num][i] = monster
            field[row_num][i + 1] = None
            if times == True:
                print("{} in lane {} advances!".format(monsters[monster_name].get("name"),list_alphabet[row_num]))
                times = False
            continue;
    return False

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field,monster_list):
    random_monster_index = random.randint(0,len(monster_list) - 1)#choose a random monster
    random_int = random.randint(0, 4)#num of row
    monster_selected = monster_list[random_monster_index]
    monster = [monster_selected,monsters[monster_selected].get("maxHP")]
    field[random_int][6] = monster #placing into field
    game_vars["num_monsters"] += 1
    return

#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
    path = "C:\\Users\\warre\\Desktop\\"
    datafile = open(path + "save.txt","w")
    #turn list into string
    datafile.write(str(field) + "\n" + str(game_vars))
    datafile.close()
    return

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game(game_vars):
    path = "C:\\Users\\warre\\Desktop\\"
    datafile = open(path + "save.txt","r")
    for line in datafile:
        temp = eval(line)
        #loads in list for draw field
        if type(temp) == list:
            field.clear()
            for item in temp:
                field.append(item)
        #loads in game_vars
        if type(temp) == dict:
            for key in temp:
                info = temp[key]
                game_vars[key] = info
            #loads in the monster buffs every 12 turns
            if game_vars["turn"]%12 == 0:
                game_vars["danger_level"] += 1
                for monster_shortnames in monster_list:
                    monsters[monster_shortnames]["min_damage"] += 1
                    monsters[monster_shortnames]["max_damage"] += 1
                    monsters[monster_shortnames]["reward"] += 1
                    monsters[monster_shortnames]["maxHP"] += 1
            
    datafile.close() 
    return

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    
    return

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------


while True:
    try:
        print("Desperate Defenders")
        print("-------------------")
        print("Defend the city from undead monsters!")
        show_main_menu()
        choice = int(input("Your Choice?"))
        if choice > 3:
            print("\n" + "No option {}".format(choice))
            continue;
        break;
    except:
        print("\n" + "entered wrong input" + "\n")
#spawn monster
spawn_monster(field,monster_list)
lose = False
while True:
    #start game
    if choice == 1:
        
        draw_field()
        show_combat_menu(game_vars)
        try:
            choice1 = int(input("Your choice? "))
            if choice1 > 4:
                print("\n" + "No option {}".format(choice1))
                continue;
        except:
            print("\n" + "entered wrong input")
            continue;
        
        if choice1 == 1: #buy unit
            unit_name = buy_unit(field, game_vars)
            #true if (3) dont buy
            if unit_name == True:
                continue;
            else:
                position = input("Place where?")
                temp = place_unit(field, position, unit_name)
                #False if places unit over another unit
                if temp == False:
                    game_vars["gold"] += defenders[unit_name].get("price")
             
        if choice1 == 2: #end turn
            game_vars["turn"] += 1
            game_vars["gold"] += 1
            threat_increase = random.randint(1, game_vars.get("danger_level"))
            game_vars["threat"] += threat_increase
            #if threat level is above 10
            if game_vars["threat"] >= game_vars["max_threat"]:
                for time in range(int(game_vars["threat"]/game_vars["max_threat"])):
                    game_vars["threat"] -= game_vars["max_threat"]
                    spawn_monster(field,monster_list)

            #every 12 turns a monster spawns
            if game_vars["turn"]%12 == 0:
                game_vars["danger_level"] += 1
                for monster_shortnames in monster_list:
                    monsters[monster_shortnames]["min_damage"] += 1
                    monsters[monster_shortnames]["max_damage"] += 1
                    monsters[monster_shortnames]["reward"] += 1
                    monsters[monster_shortnames]["maxHP"] += 1
    
            row_num = 0
            for row in field:
                column = 0
                for item in row:
                    if item != None:
                        if item[0] in defender_list:
                            defender_name = item[0]
                            defender_attack(defender_name, field, row_num, column)
                            
                        if item[0] in monster_list:
                            monster_name = item[0]
                            #when True, lost
                            lose = monster_advance(monster_name, field, row_num, column)
                            if lose == True:
                                break;
                    column += 1
                row_num += 1
            #player loses
            if lose == True:
                break;
            
            #After player kills 20 monster(win condition)
            if game_vars.get('monsters_killed') == 20:
                print("You have protected the city! You win!")
                break;

            #when there is no more monsters on the field
            if game_vars.get("num_monsters") == 0:
                spawn_monster(field,monster_list)
                
        if choice1 == 3: #save_game
            save_game()
            print("\n" + "\n" + "Game saved!")
            continue;
        if choice1 == 4: #Quit_game
            print("\n" + "\n" +"See you next time!")
            break;   
            
    elif choice == 2:
        load_game(game_vars)
        choice = 1
    elif choice == 3:
        save_game()
# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
    
    
