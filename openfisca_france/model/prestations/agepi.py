from datetime import date
import numpy as np

from openfisca_france.model.base import Famille, Individu, Variable, Enum, MONTH, \
     set_input_dispatch_by_period, set_input_divide_by_period, min_, not_


class pe_nbenf(Variable):
    value_type = int
    entity = Famille
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Nombre d'enfants pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    reference = [
        "Article 2 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
        ]

    def formula(famille, period):
        age_enfant_eligible = famille('agepi_eligible', period)
        nb_enfants_eligibles = famille.sum(age_enfant_eligible, role=Famille.ENFANT)
        return nb_enfants_eligibles


class agepi_temps_travail_semaine(Variable):
    value_type = float
    entity = Individu
    label = "Temps de travail par semaine pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        heures_remunerees_volume = individu('heures_remunerees_volume', period)
        return heures_remunerees_volume / 52 * 12  # Passage en heures par semaine


class agepi_percue_12_derniers_mois(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu a t-il perçu une AGEPI dans les 12 derniers mois"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class emploi_ou_formation_en_france(Variable):
    value_type = bool
    entity = Individu
    label = "L'emploi ou la formation de l'individu se situe en France"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesCategoriesDemandeurEmploi(Enum):
    __order__ = 'pas_de_categorie categorie_1 categorie_2 categorie_3 categorie_4_stagiaire_formation_professionnelle categorie_5_contrat_aide categorie_6 categorie_7 categorie_8' \
                # Needed to preserve the enum order in Python 2
    pas_de_categorie = "Aucune catégorie"
    categorie_1 = "Catégorie 1 - Personnes sans emploi, immédiatement disponibles en recherche de CDI plein temps."
    categorie_2 = "Catégorie 2 - Personnes sans emploi, immédiatement disponibles en recherche de CDI à temps partiel."
    categorie_3 = "Catégorie 3 - Personnes sans emploi, immédiatement disponibles en recherche de CDD."
    categorie_4_stagiaire_formation_professionnelle = "Catégorie 4 - stagiaire de la formation professionnelle - Personnes sans emploi, non immédiatement disponibles et à la recherche d’un emploi."
    categorie_5_contrat_aide = "Catégorie 5 - contrat aidé - Personnes non immédiatement disponibles, parce que titulaires d'un ou de plusieurs emplois, et à la recherche d'un autre emploi."
    categorie_6 = "Catégorie 6 - Personnes non immédiatement disponibles, en recherche d'un autre emploi en CDI à plein temps."
    categorie_7 = "Catégorie 7 - Personnes non immédiatement disponibles, en recherche d'un autre emploi en CDI à temps partiel."
    categorie_8 = "Catégorie 8 - Personnes non immédiatement disponibles, en recherche d'un autre emploi en CDD."


class pole_emploi_categorie_demandeur_emploi(Variable):
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-n2016-33-du-6-octobr.html?type=dossiers/2016/bope-n2016-80-du-17-novembre-201#",
        "Annexe 3 : la fiche 3 - Les effets de l’inscription"
        ]
    value_type = Enum
    possible_values = TypesCategoriesDemandeurEmploi
    default_value = TypesCategoriesDemandeurEmploi.pas_de_categorie
    entity = Individu
    label = "Le classement des demandeurs d’emploi dans les différentes catégories d’inscription à Pôle Emploi"
    definition_period = MONTH


class reside_en_region_mayotte(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu réside en région Mayotte"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesActiviteCondition(Enum):
    __order__ = 'aucune_activite cdi cdd ctt formation'  # Needed to preserve the enum order in Python 2
    aucune_activite = "AUCUNE ACTIVITE"
    cdi = "CDI"
    cdd = "CDD"
    ctt = "CTT"
    formation = "FORMATION"


class types_activite_condition(Variable):
    value_type = Enum
    possible_values = TypesActiviteCondition
    default_value = TypesActiviteCondition.aucune_activite
    entity = Individu
    label = "Les types d'activité éligibles à l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI "
    definition_period = MONTH


class TypesIntensiteActivite(Enum):
    __order__ = 'intensite_non_valide hebdomadaire mensuelle'  # Needed to preserve the enum order in Python 2
    intensite_non_valide = "INTENSITE_NON_VALIDE"
    hebdomadaire = "HEBDOMADAIRE"
    mensuelle = "MENSUELLE"


class types_intensite_activite(Variable):
    value_type = Enum
    possible_values = TypesIntensiteActivite
    default_value = TypesIntensiteActivite.mensuelle
    entity = Individu
    label = "Les types d'intensité pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI "
    definition_period = MONTH


class agepi_date_demande(Variable):
    value_type = date
    default_value = date(1870, 1, 1)
    entity = Individu
    label = "Date de demande d'évaluation à l'éligibilité à l'AGEPI (date du fait générateur)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"


class agepi_eligible(Variable):
    value_type = bool
    entity = Famille
    label = "Eligibilité à l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
        ]
    documentation = '''
        1- L'individu élève seul son enfant dont l'âge est inférieur à 10 ans (condition de garde d'enfant)
        2- L'individu n'a pas touché l'AGEPI dans les 12 derniers mois (condition de durée entre faits générateurs)
        3- L'individu est inscrit en catégorie 1, 2, 3, 4 "stagiaire de la formation professionnelle" ou 5 "contrat aidé"
        4- L'emploi ou la formation se situe en France
        5- L'individu effectue sa demande au plus tard dans le mois qui suit sa reprise d'emploi ou de formation
        6- L'individu est non indemnisé ou son ARE est inférieure ou égale à l'ARE minimale
        7- L'individu est en reprise d'emploi du type CDI, CDD ou CTT d'au moins 3 mois consécutifs ou en processus d'entrée en formation d'une durée supérieure ou égale à 40 heures
    '''

    def formula(famille, period, parameters):

        #  Diminution de la précision car la comparaison : 14.77 <= 14.77 me renvoyait un False

        epsilon = 0.001

        #  1
        parents_isoles = famille('nb_parents', period) == 1

        age_enfants = famille.members('age', period)
        age_enfants_eligible = (age_enfants < parameters(period).prestations.agepi.age_enfant_maximum) * (age_enfants > 0)

        #  2

        agepi_non_percues = not_(famille.members('agepi_percue_12_derniers_mois', period))

        #  3

        pe_categorie_demandeur_emploi = famille.members('pole_emploi_categorie_demandeur_emploi', period)

        categories_eligibles = ((pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_1)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_2)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_3)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_4_stagiaire_formation_professionnelle)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_5_contrat_aide)
                                + (not_(pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_6))
                                * (not_(pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_7))
                                * (not_(pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_8))
                                * (not_(pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.pas_de_categorie)))

        #  4

        reprises_activites_en_france = famille.members('emploi_ou_formation_en_france', period)

        #  5

        contrat_de_travail_debut = famille.members('contrat_de_travail_debut', period)  # numpy.datetime64
        contrat_de_travail_debut_en_mois = contrat_de_travail_debut.astype('M8[M]')
        print("contrat_de_travail_debut_en_mois = ", contrat_de_travail_debut_en_mois)

        date_limite_eligibilite_contrat = min_(
            (contrat_de_travail_debut_en_mois + 1) + (contrat_de_travail_debut - contrat_de_travail_debut_en_mois), 
            (contrat_de_travail_debut_en_mois + 2) - np.timedelta64(1, 'D')
            )
        print("date_limite_eligibilite_contrat = ", date_limite_eligibilite_contrat)
        
        agepi_date_demande = famille.members("agepi_date_demande", period)
        date_demande_agepi_eligible = agepi_date_demande <= date_limite_eligibilite_contrat
        print("date_demande_agepi_eligible", date_demande_agepi_eligible)

        #  6

        resident_en_mayotte = famille.members('reside_en_region_mayotte', period) == 1
        ne_resident_pas_en_mayotte = not_(resident_en_mayotte)

        allocation_individu = famille.members('allocation_retour_emploi', period)

        allocation_minimale_hors_mayotte = parameters(period).allocation_retour_emploi.montant_minimum_hors_mayotte * ne_resident_pas_en_mayotte
        allocation_minimale_mayotte = parameters(period).allocation_retour_emploi.montant_minimum_mayotte * resident_en_mayotte

        allocation_minimale_en_fonction_de_la_region = allocation_minimale_hors_mayotte + allocation_minimale_mayotte

        #  Montant ARE minimum en fonction de la région (Mayotte / hors Mayotte)

        are_individu_egale_are_min = np.fabs(allocation_individu - allocation_minimale_en_fonction_de_la_region) < epsilon
        are_individu_inferieure_are_min = allocation_individu < allocation_minimale_en_fonction_de_la_region

        montants_are_eligibles = are_individu_inferieure_are_min + are_individu_egale_are_min

        #  7

        reprises_types_activites = famille.members('types_activite_condition', period)

        reprises_types_activites_aucune_activite = not_(reprises_types_activites == TypesActiviteCondition.aucune_activite)
        reprises_types_activites_formation = reprises_types_activites == TypesActiviteCondition.formation
        reprises_types_activites_cdi = reprises_types_activites == TypesActiviteCondition.cdi
        reprises_types_activites_cdd = reprises_types_activites == TypesActiviteCondition.cdd
        reprises_types_activites_ctt = reprises_types_activites == TypesActiviteCondition.ctt

        #  La formation doit être supérieure ou égale à 40 heures
        duree_formation = famille.members('heures_remunerees_volume', period)
        periode_formation_eligible = duree_formation >= parameters(period).prestations.agepi.duree_de_formation_minimum

        #  Le durée de contrat de l'emploi doit être d'au moins 3 mois
        periode_de_contrat_3_mois_minimum = famille.members('contrat_de_travail_duree', period) >= 3

        reprises_types_activites_formation_eligible = reprises_types_activites_formation * periode_formation_eligible
        reprises_types_activites_cdd_eligible = reprises_types_activites_cdd * periode_de_contrat_3_mois_minimum
        reprises_types_activites_ctt_eligible = reprises_types_activites_ctt * periode_de_contrat_3_mois_minimum

        types_et_duree_activite_eligible = reprises_types_activites_aucune_activite \
            * (reprises_types_activites_formation_eligible
            + reprises_types_activites_cdi
            + reprises_types_activites_cdd_eligible
            + reprises_types_activites_ctt_eligible)

        # date_demande_agepi_eligible = True

        return parents_isoles \
            * age_enfants_eligible \
            * agepi_non_percues \
            * reprises_activites_en_france \
            * categories_eligibles \
            * date_demande_agepi_eligible \
            * montants_are_eligibles \
            * types_et_duree_activite_eligible != 0


class agepi(Variable):
    value_type = float
    entity = Famille
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20",
        "2. Aide à la garde d’enfants pour les parents isolés (AGEPI)",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-dg-n2014-48-du-6-jui.html?type=dossiers/2014/bope-n2014-62-du-18-juin-2014"
        ]

    def formula(famille, period, parameters):
        types_de_contrat = famille.members('types_activite_condition', period)
        contrat_cdi = types_de_contrat == TypesActiviteCondition.cdi
        contrat_autre_que_cdi = not_(types_de_contrat == TypesActiviteCondition.cdi)
        intensite_activite = famille.members('types_intensite_activite', period)
        nb_heures_semaine = famille.sum(famille.members('agepi_temps_travail_semaine', period), role=Famille.PARENT)
        nb_heures_mensuelles = famille.members('heures_remunerees_volume', period)
        nb_enfants_eligibles = famille('pe_nbenf', period)
        eligibilite_agepi = famille('agepi_eligible', period)

        intensite_hebdomadaire = intensite_activite == TypesIntensiteActivite.hebdomadaire
        intensite_mensuelle = intensite_activite == TypesIntensiteActivite.mensuelle

        resident_en_mayotte = famille.members('reside_en_region_mayotte', period) == 1
        ne_resident_pas_en_mayotte = not_(resident_en_mayotte)

        #  Montants en fonction de la région avec ou sans prise en compte de l'intensite
        montants_hors_mayotte = parameters(period).prestations.agepi.montants.hors_mayotte
        montants_mayotte = parameters(period).prestations.agepi.montants.mayotte

        montant_maximum_hors_intensite_hors_mayotte = montants_hors_mayotte.maximum.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte
        montant_maximum_hors_intensite_mayotte = montants_mayotte.maximum.calc(nb_enfants_eligibles) * resident_en_mayotte

        ################################################################################################################

        #  Montants en fonction du nombre d'enfants pour une reprise emploi ou formation < 15h/sem - HORS MAYOTTE
        montants_minimum_intensite_hebdo_hors_mayotte = montants_hors_mayotte.minimum.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte * intensite_hebdomadaire
        montants_maximum_intensite_hebdo_hors_mayotte = montants_hors_mayotte.maximum.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte * intensite_hebdomadaire

        #  Montants en fonction du nombre d'enfants pour une reprise emploi ou formation < 64h/mensuelle - HORS MAYOTTE
        montants_minimum_intensite_mensuelle_hors_mayotte = montants_hors_mayotte.minimum.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte * intensite_mensuelle
        montants_maximum_intensite_mensuelle_hors_mayotte = montants_hors_mayotte.maximum.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte * intensite_mensuelle

        ################################################################################################################

        #  Montants en fonction du nombre d'enfants pour une reprise emploi ou formation < 15h/sem - MAYOTTE
        montants_minimum_intensite_hebdo_mayotte = montants_mayotte.minimum.calc(nb_enfants_eligibles) * resident_en_mayotte * intensite_hebdomadaire
        montants_maximum_intensite_hebdo_mayotte = montants_mayotte.maximum.calc(nb_enfants_eligibles) * resident_en_mayotte * intensite_hebdomadaire

        #  Montants en fonction du nombre d'enfants pour une reprise emploi ou formation < 64h/mensuelle - MAYOTTE
        montants_minimum_intensite_mensuelle_mayotte = montants_mayotte.minimum.calc(nb_enfants_eligibles) * resident_en_mayotte * intensite_mensuelle
        montants_maximum_intensite_mensuelle_mayotte = montants_mayotte.maximum.calc(nb_enfants_eligibles) * resident_en_mayotte * intensite_mensuelle

        ################################################################################################################

        #  Montants minorés / majorés - Hors Mayotte - intensité hebdomadaire
        montants_minimums_hors_mayotte = montants_minimum_intensite_hebdo_hors_mayotte + montants_minimum_intensite_mensuelle_hors_mayotte
        montants_maximums_hors_mayotte = montants_maximum_intensite_hebdo_hors_mayotte + montants_maximum_intensite_mensuelle_hors_mayotte

        #  Montants minorés / majorés - Mayotte - intensité mensuelle
        montants_minimums_mayotte = montants_minimum_intensite_hebdo_mayotte + montants_minimum_intensite_mensuelle_mayotte
        montants_maximums_mayotte = montants_maximum_intensite_hebdo_mayotte + montants_maximum_intensite_mensuelle_mayotte

        #  Association des tableaux de montants - Hors Mayotte / Mayotte - intensité hebdomadaire / mensuelle

        montants_minimums_en_fonction_de_la_region = montants_minimums_hors_mayotte + montants_minimums_mayotte
        montants_maximums_en_fonction_de_la_region = montants_maximums_hors_mayotte + montants_maximums_mayotte

        ################################################################################################################

        # Calcul du montant en fonction du nombre d'heures de la reprise d'emploi ou de formation

        condition_montants_minimums_hebdomadaire = (nb_heures_semaine < 15) * intensite_hebdomadaire
        condition_montants_minimums_mensuelle = (nb_heures_mensuelles < 64) * intensite_mensuelle

        condition_montants_maximums_hebdomadaire = (nb_heures_semaine >= 15) * intensite_hebdomadaire
        condition_montants_maximums_mensuelle = (nb_heures_mensuelles >= 64) * intensite_mensuelle

        condition_montants_minimums = condition_montants_minimums_hebdomadaire + condition_montants_minimums_mensuelle
        condition_montants_maximums = condition_montants_maximums_hebdomadaire + condition_montants_maximums_mensuelle

        ################################################################################################################

        montant_avec_intensite = ((condition_montants_minimums * montants_minimums_en_fonction_de_la_region)
            + (condition_montants_maximums * montants_maximums_en_fonction_de_la_region)) * contrat_autre_que_cdi

        # Si activite CDI, on ne prend pas en compte l'intensite

        montant_sans_intensite = (montant_maximum_hors_intensite_hors_mayotte + montant_maximum_hors_intensite_mayotte) * contrat_cdi

        montants = montant_avec_intensite + montant_sans_intensite

        return eligibilite_agepi * montants
