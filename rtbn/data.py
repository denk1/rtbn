from rtbn.models import Person, \
                                               Mobilization, \
                                               MilitaryEnlistmentOffice, \
                                               AddressItem, \
                                               CallingTeam, \
                                               WarUnit, \
                                               WarServe


def find_address(type_place, place_name):
    places = places.objects.filter(address_item_type=type_place, region_name__iexact=place_name)
    if places.count() > 0:
        return places[0]
    else:
        return None


def fill_address(address, address_type):
    is_new = False
    addr_prev = None
    addr = None
    for i in range(len(address)):
        addr = find_address(address_data[i], address_type[i])
        if addr is None:
            addr = address_data[i].objects.create(address_item_name = address[i], address_item_type=address_type[i], above_address_unit=addr_prev)
        addr_prev = addr
    return addr


def find_warunit(warunit_name, warunit_type):
    war_units = WarUnit.objects.filter(name__iexact=warunit_name,
                                       warunit_type=warunit_type)
    if war_units.count() > 0:
        return war_units[0], True
    
    war_units = WarUnit.objects.filter(name__iexact=warunit_name)
    if war_units.count() > 0:
        return war_units[0], False
    return None, None


def fill_warunit(name_warunit_dict):
    prev_warunit = None
    warunit = None
    i = 0
    for u in name_warunit_dict.keys():
        if name_warunit_dict[u] is not None:
            finded_unit, flag_type = find_warunit(name_warunit_dict[u], u)
            if finded_unit is not None and flag_type is not None:
                warunit = finded_unit
            else:
                if i == 0:
                    warunit = WarUnit.objects.create(above_war_unit=None, 
                                       name = name_warunit_dict[u],
                                       warunit_type=u)
                else:
                    warunit = WarUnit.objects.create(above_war_unit=None, 
                                       name = name_warunit_dict[u],
                                       warunit_type=u)
            i = i + 1
            prev_warunit = warunit
    return warunit


def fill_new_line(post_obj):
    # person
    surname = post_obj.get('surname')
    surname_distortion = post_obj.get('surname_distortion')
    name = post_obj.get('name')
    name_distortion = post_obj.get('name_distortion')
    father_name = post_obj.get('father_name')
    father_name_distortion = post_obj.get('father_name_distortion')
    birthday = post_obj.get('birthday')
    born_region_name = post_obj.get('born_region_name')
    born_district_name = post_obj.get('born_district_name')
    born_locality_name = post_obj.get('born_locality_name')
    born_region_type = post_obj.get('born_region_type')
    born_district_type = post_obj.get('born_district_type')
    born_locality_type = post_obj.get('born_locality_type')
    born_address = [born_region_name, born_district_name, born_locality_name]
    born_address_type = [born_region_type, born_district_type, born_locality_type]
    #born address
    born_locality = fill_address(born_address, born_address_type)
    live_region_name = post_obj.get('live_region_name')
    live_district_name = post_obj.get('live_district_name')
    live_locality_name = post_obj.get('live_locality_name')
    live_region_type = post_obj.get('live_region_type')
    live_district_type = post_obj.get('live_district_type')
    live_locality_type = post_obj.get('live_localuty_type')
    live_address = [live_region_name, live_district_name, live_locality_name]
    live_address_type = [live_region_type, live_district_type, live_locality_type]
    #live address
    live_locality = fill_address(live_address, live_address_type)

    # mobilization
    date_mobilization = post_obj.get("date_mobilization")
    region_military_enlistment_office = post_obj.get('region_military_enlistment_office')
    district_military_enlistment_office = post_obj.get('district_military_enlistment_office')
    region_type_military_enlistment_office = post_obj.get('region_type_military_enlistment_office')
    district_type_military_enlistment_office = post_obj.get('district_type_military_enlistment_office')
    military_enlistment_office_district = fill_address([region_military_enlistment_office,
                                              district_military_enlistment_office,], 
                                              [region_type_military_enlistment_office,
                                               district_type_military_enlistment_office,
                                              ])
    
    
    military_enlistment_name = post_obj.get('military_enlistment')
    military_enlistment_office = MilitaryEnlistmentOffice.objects.create(address=military_enlistment_office_district,
                                                                         name=military_enlistment_name)

    calling_team_name = post_obj.get("calling_team_name")

    direction_front_name = post_obj.get('direction_front_name')
    direction_army_name = post_obj.get('direction_army_name')
    direction_warunit = post_obj.get('warunit_name')
    last_msg_region = post_obj.get('last_msg_region')
    last_msg_region_type = post_obj.get('last_msg_region_type')
    last_msg_district = post_obj.get('last_msg_district')
    last_msg_district_type = post_obj.get('last_msg_district_type')
    last_msg_locality = post_obj.get('last_msg_locality')
    last_msg_locality_type = post_obj.get('last_msg_locality_type')
    last_msg_address = [last_msg_region, last_msg_district, last_msg_locality]
    last_msg_address_types = [last_msg_region_type, last_msg_district_type, last_msg_locality_type]
    last_msg_locality = fill_address(last_msg_address, last_msg_address_types)
    direction_dict = {WarUnitType.FRONT: direction_front_name,
                      WarUnitType.ARMY: direction_army_name,
                      WarUnitType.DIVISION: None,
                      WarUnitType.RGT: None,
                      WarUnitType.COY: None,
                      WarUnitType.UNIT: direction_warunit }
    warunit_direction = fill_warunit(direction_dict)
    calling_team = CallingTeam.objects.create(name = calling_team_name)
    mobilization = Mobilization.objects.create(date_mobilization=date_mobilization)
    call = Call.objects.create(military_enlistment_office=military_enlistment_office,
                               moblization=mobilization,
                               warunit=warunit,
                               last_msg_locality=last_msg_locality)
    new_person = Person.objects.create(
                          name=name, 
                          name_distortion=name_distortion,
                          surname=surname, 
                          surname_distortion=surname_distortion,
                          father_name=father_name_distortion,
                          father_name_distortion=father_name_distortion,
                          born_locality=born_locality,
                          live_locality=live_locality,
                          call=call)
    calling_team_direction = CallingTeamDirection.objects.create(calling_team=calling_team, person=new_person)
    calling_team_direction.save()

    fight_since_list = post_obj.getlist('fight_since[]')
    fight_to_list = post_obj.getlist('fight_to[]')
    army_name_list = post_obj.getlist('army_name[]')
    division_name_list = post_obj.getlist('division_name[]')
    regiment_name_list = post_obj.getlist('regiment_name[]')
    company_name_list = post_obj.getlist('company_name[]')
    platoon_name_list = post_obj.getlist('platoon_name[]')



    fights_size = len(fight_since_list)
    for i in range(fights_size):
        
        pass
        #WarArchievement.objects.create(war_operation=military_operation_name[i],
        #                               )
        

    

    
    


    
     





