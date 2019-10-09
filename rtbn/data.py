from rtbn.models import Person, \
                        Mobilization, \
                        MilitaryEnlistmentOffice, \
                        AddressItem, \
                        CallingTeam, \
                        WarUnit, \
                        WarServe, \
                        WarOperation, \
                        Hospital, \
                        Hospitalization, \
                        CampArbeit, \
                        InfirmaryCamp, \
                        AddingInfo, \
                        Burial, \
                        Reburial


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
    is_new = False
    i = 0
    for u in name_warunit_dict.keys():
        if name_warunit_dict[u] is not None:
            finded_unit, flag_type = find_warunit(name_warunit_dict[u], u)
            if finded_unit is not None and flag_type is not None and is_new is False:
                warunit = finded_unit
            else:
                warunit = WarUnit.objects.create(above_war_unit=None, 
                                       name = name_warunit_dict[u],
                                       warunit_type=u)
                is_new = True
            prev_warunit = warunit
    return warunit


def fill_new_line(post_obj):
    # ######################
    # the personal data - N1
    # ######################
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

    # ####################
    # mobilization - N2
    # ####################
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
    #it's creating of the record into CallingTeam table
    calling_team = CallingTeam.objects.create(name = calling_team_name)
    #it's creating of the record into Mobilization
    mobilization = Mobilization.objects.create(date_mobilization=date_mobilization)
    #Call
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
    new_person.save()

    calling_team_direction = CallingTeamDirection.objects.create(calling_team=calling_team, person=new_person)
    calling_team_direction.save()
    # ########################
    # The fighting action - N3
    # ########################
    military_operations_list = post_obj.getlist('military_operation_name[]')
    fight_since_list = post_obj.getlist('fight_since[]')
    fight_to_list = post_obj.getlist('fight_to[]')
    front_name_list = post_obj.getlist('front_name[]')
    army_name_list = post_obj.getlist('army_name[]')
    division_name_list = post_obj.getlist('division_name[]')
    regiment_name_list = post_obj.getlist('regiment_name[]')
    company_name_list = post_obj.getlist('company_name[]')
    platoon_name_list = post_obj.getlist('platoon_name[]')


    fights_size = len(fight_since_list)
    for i in range(fights_size):
        military_operation = military_operations_list[i]
        fight_since = fight_since_list[i]
        fight_to = fight_to[i]
        front_name = front_name_list[i]
        army_name = army_name_list[i]
        division_name = division_name_list[i]
        regiment_name = regiment_name_list[i]
        company_name = company_name_list[i]
        platoon_name = platoon_name_list[i]
        unit_dict = { WarUnitType.FRONT: front_name,
                      WarUnitType.ARMY: army_name,
                      WarUnitType.DIVISION: division_name,
                      WarUnitType.RGT: regiment_name,
                      WarUnitType.COY: company_name,
                      WarUnitType.UNIT: platoon_name
        }
        war_serve_unit = fill_warunit(unit_dict)
        war_serve = WarServe.objects.create(person=new_person, war_unit=war_serve_unit)
        war_serve.save()
        war_operation = WarOperation.objects.create(name=military_operation)
        war_operation.save()
        war_archievenment = WarArchievenment.objects.create(war_operation=war_operation,
                                                            war_serve=war_serve,
                                                            period_from=fight_since,
                                                            period_to=fight_to)
        war_archievenment.save()
                                    
    # ########################
    # the hospitalization - N4
    # ########################
    hospital_name_list = post_obj.get('hospital_name[]')
    hospital_period_since_list = post_obj.get('hospital_since[]')
    hospital_period_to_list = post_obj.get('hospital_to[]')
    hospital_region_list = post_obj.get('hospital_region_name[]')
    hospital_district_list = post_obj.get('hospital_district_name[]')
    hospital_locality_list = post_obj.get('hospital_locality_name[]')
    hospital_army_list = post_obj.get('hospital_army_name[]')
    hospital_division_list = post_obj.get('hospital_division_name[]')
    hospital_regiment_list = post_obj.get('hospital_regiment_name[]')
    healthy_direction_list = post_obj.get('healthy_direction[]')
    hospital_size = len(hospital_name_list)
    for i in range(hospital_size):
        hospital = Hospital.objects.create(name=hospital_name_list)
        war_unit_consist_dict = {WarUnitType.FRONT: None,
                                 WarUnitType.ARMY: hospital_army_list[i],
                                 WarUnitType.DIVISION: hospital_division_list[i],
                                 WarUnitType.RGT: hospital_regiment_list[i],
                                 WarUnitType.COY: None,
                                 WarUnitType.UNIT: None }
        war_unit_consist = fill_warunit(war_unit_consist)
        hospitalization = Hospitalization.objects.create(person=new_person,
                                                         hospital=hospital,
                                                         period_from=hospital_period_since_list[i],
                                                         period_to=hospital_period_to_list[i],
                                                         war_unit_consis=war_unit_consist,
                                                         direction_name=healthy_direction_list[i]
                                                         )
    # ############################
    # The captivity - N5
    # ############################
    date_of_captivity_list = post_obj.get('date_of_captivity[]')
    capt_region_list = post_obj.get('capt_region[]')
    capt_region_type_list = post_obj.get('capt_region_type[]')
    capt_district_list = post_obj.get('capt_district[]')
    capt_district_type_list = post_obj.get('capt_district_type[]') 
    capt_locality_list = post_obj.get('capt_locality[]')
    capt_locality_type_list = post_obj.get('capt_locality_type[]')
    camps_list = post_obj.get('camp[]')
    count_captivities = len(camps_list)
    number_of_prisoners_list = post_obj.get('number_of_prisoners')
    for i in range(count_captivities):
        capt_region = capt_region_list[i]
        capt_region_type = capt_region_type_list[i]
        capt_district = capt_district_list[i]
        capt_district_type = capt_district_type_list[i]
        capt_locality = capt_locality_list[i]
        capt_locality_type = capt_locality_type_list[i]
        capt_address = [capt_region, capt_district, capt_locality]
        capt_address_type = [capt_region_type, capt_district_type, capt_locality_type]
        capt_locality = fill_address(capt_address, capt_address_type)
        camp = Camp.objects.create(name=camps_list[i],
                                   number=number_of_prisoners_list[i])
        captivity = Captivity.objects.create(person=new_person,
                                 date_of_captivity=date_of_captivity_list[i],
                                 place_of_captivity=capt_locality,
                                 camp=camp
                                 )
        camp_arbeit_list = post_obj.get('work_command[][]')
        period_from_list = post_obj.get('work_since[][]')
        period_to_list = post_obj.get('work_to[][]')
        camp_arbeit_count = len(camp_arbeit_count[i])
        for j in range(camp_arbeit_count):
            camp_arbeit = camp_arbeit_list[i][j]
            period_from = period_from_list[i][j]
            period_to = period_to_list[i][j]
            camp_arbeit = CampArbeit.objects.create(
                                      camp=camp,
                                      name=camp_arbeit,
                                      period_from=period_from,
                                      period_to=period_to,
                                      captivity=captivity
                                      )
            camp_arbeit.save()
        
        infirmary_camp_list = post_obj.get('infirmary[][]')
        period_from_list = post_obj.get('infir_since[][]')
        period_to_list = post_obj.get('infir_to[][]')
        infirmary_count = len(infirmary_camp_list[i])
        for j in range(infirmary_count):
            infirmary_camp = infirmary_camp_list[i][j]
            period_from = period_from_list[i][j]
            period_to = period_to[i][j]
            infirmary = InfirmaryCamp.objects.create(camp=camp,
                                         period_from=period_from,
                                         period_to=period_to,
                                         captivity=captivity,
                                         name = infirmary_camp
                                         )
            infirmary.save()
        camp.save()
        captivity.save()
    is_defector = post_obj.get('defector')
    is_gestapo = post_obj.get('gestapo')
    is_frei = post_obj.get('frei')
    adding_info = AddingInfo.objects.create(
                              person=new_person,
                              is_defector=is_defector,
                              is_gestapo=is_gestapo,
                              is_frei=is_frei
                             )
    adding_info.save()

    # ###########################
    # The bureal - N6
    # ###########################
    date_of_burial = post_obj.get('date_of_burial')
    burial_region_doc = post_obj.get('burial_region_doc')
    burial_region_type_doc = post_obj.get('burial_region_doc_type')
    burial_district_doc = post_obj.get('burial_disrict_doc')
    burial_district_type_doc = post_obj.get('burial_district_type_doc')
    burial_locality_doc = post_obj.get('burial_locality_doc')
    burial_locality_type_doc = post_obj.get('burial_locality_type_doc')
    burial_doc_address_list = [burial_region_doc, burial_district_doc, burial_locality_doc]
    burial_doc_address_types_list = [burial_region_type_doc, burial_district_type_doc, burial_locality_type_doc]
    burial_doc_address = fill_address(burial_doc_address_list, burial_doc_address_types_list)
    burial_region_act = post_obj.get('burial_region_act')
    burial_region_type_act = post_obj.get('burial_region_act_type')
    burial_district_act = post_obj.get('burial_disrict_act')
    burial_district_type_act = post_obj.get('burial_district_type_act')
    burial_locality_act = post_obj.get('burial_locality_act')
    burial_locality_type_act = post_obj.get('burial_locality_type_act')
    burial_act_address_list = [burial_region_act, burial_district_act, burial_locality_act]
    burial_act_address_types_list = [burial_region_type_doc, burial_district_type_doc, burial_locality_type_doc]
    burial_act_address = fill_address(burial_doc_address_list, burial_doc_address_types_list)
    #defenition of the burial
    cemetery = post_obj.get('cemetery')
    number_plot = post_obj.get('number_plot')
    number_line = post_obj.get('number_line')
    number_thumb = post_obj.get('number_thumb')
    burial = Burial.objects.create(person=new_person,
                          date_of_burial=date_of_burial,
                          address_doc=burial_doc_address,
                          address_act=burial_act_address,
                          cemetery=cemetery,
                          number_plot=number_plot,
                          number_line=number_line,
                          number_thumb=number_thumb)
    burial.save()
    #reburial
    date_of_reburial = post_obj.get('date_of_reburial')
    rebureal_cause = post_obj.get('reburial_cause')
    reburial_region_fact = post_obj.get('capt_region[]')
    reburial_region_type_fact = post_obj.get('capt_region_type[]')
    reburial_district_fact = post_obj.get('capt_district[]')
    reburial_district_type_fact = post_obj.get('capt_district_type[]') 
    reburial_locality_fact = post_obj.get('capt_locality[]')
    reburial_locality_type_fact = post_obj.get('capt_locality_type[]')
    reburial_fact_address_list = [reburial_region_fact, reburial_district_fact, burial_locality_act]
    reburial_fact_address_types_list = [reburial_region_type_fact, reburial_district_type_fact, reburial_locality_type_fact]
    reburial_fact_address = fill_address(reburial_fact_address_list, reburial_fact_address_types_list)
    reburial = Reburial.objects.create(burial=burial,
                            date_of_reburial=date_of_reburial,
                            rebureal_cause=rebureal_cause,
                            address=reburial_fact_address)
    reburial.save()

    



    

    
    


    
     





