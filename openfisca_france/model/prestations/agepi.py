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

    def formula(famille, period, parameters):
        age_membres_famille = famille.members('age', period)
        age_eligibles = (age_membres_famille < parameters(period).prestations.agepi.age_enfant_maximum) * (age_membres_famille > 0)
        nb_enfants_eligibles = famille.sum(age_eligibles, role=Famille.ENFANT)

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
    __order__ = 'pas_de_categorie categorie_1 categorie_2 categorie_3 categorie_4 categorie_5 categorie_6 categorie_7 categorie_8' \
                # Needed to preserve the enum order in Python 2
    pas_de_categorie = "Aucune catégorie"
    categorie_1 = "Catégorie 1 - Personnes sans emploi, immédiatement disponibles en recherche de CDI plein temps."
    categorie_2 = "Catégorie 2 - Personnes sans emploi, immédiatement disponibles en recherche de CDI à temps partiel."
    categorie_3 = "Catégorie 3 - Personnes sans emploi, immédiatement disponibles en recherche de CDD."
    categorie_4 = "Catégorie 4 - Personnes sans emploi, non immédiatement disponibles et à la recherche d’un emploi."
    categorie_5 = "Catégorie 5 - Personnes non immédiatement disponibles, parce que titulaires d'un ou de plusieurs emplois, et à la recherche d'un autre emploi."
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


class en_contrat_aide(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est en contrat aidé"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesContrat(Enum):
    __order__ = 'aucune_activite cdi cdd ctt formation'  # Needed to preserve the enum order in Python 2
    aucune_activite = "AUCUNE ACTIVITE"
    cdi = "CDI"
    cdd = "CDD"
    ctt = "CTT"
    formation = "FORMATION"


class types_activite_condition(Variable):
    value_type = Enum
    possible_values = TypesContrat
    default_value = TypesContrat.aucune_activite
    entity = Individu
    label = "Les types d'activité éligibles à l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI "
    definition_period = MONTH


class TypesIntensiteActivite(Enum):
    __order__ = 'intensite_non_valide sans_intensite hebdomadaire mensuelle'  # Needed to preserve the enum order in Python 2
    intensite_non_valide = "INTENSITE_NON_VALIDE"
    sans_intensite = "SANS_INTENSITE"
    hebdomadaire = "HEBDOMADAIRE"
    mensuelle = "MENSUELLE"


class types_intensite_activite(Variable):
    value_type = Enum
    possible_values = TypesIntensiteActivite
    default_value = TypesIntensiteActivite.mensuelle
    entity = Individu
    label = "Les types d'intensité pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
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
    entity = Individu
    label = "Eligibilité à l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
        ]
    documentation = '''
        1- L'individu élève seul son enfant (parent isolé)
        2- L'âge du ou des enfants dont il a la garde est inférieur à 10 ans (condition de garde d'enfant)
        3- L'individu n'a pas touché l'AGEPI dans les 12 derniers mois (condition de durée entre faits générateurs)
        4- L'individu est inscrit en catégorie 1, 2, 3, 4 "stagiaire de la formation professionnelle" ou 5 "contrat aidé"
        5- L'emploi ou la formation se situe en France
        6- L'individu effectue sa demande au plus tard dans le mois qui suit sa reprise d'emploi ou de formation
        7- L'individu est non indemnisé ou son ARE est inférieure ou égale à l'ARE minimale
        8- L'individu est en reprise d'emploi du type CDI, CDD ou CTT d'au moins 3 mois consécutifs ou en processus d'entrée en formation d'une durée supérieure ou égale à 40 heures
    '''

    def formula(individu, period, parameters):

        #  Diminution de la précision car la comparaison : 14.77 <= 14.77 me renvoyait un False

        epsilon = 0.0001

        #  1
        parents_isoles = individu.famille('nb_parents', period) == 1

        #  2
        condition_nb_enfants = individu.famille('pe_nbenf', period) > 0

        #  3
        agepi_non_percues = not_(individu('agepi_percue_12_derniers_mois', period))

        #  4
        pe_categorie_demandeur_emploi = individu('pole_emploi_categorie_demandeur_emploi', period)

        stagiaire_formation_professionnelle = individu('stagiaire', period)
        contrat_aide = individu('en_contrat_aide', period)

        categorie_4 = pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_4
        categorie_4_stagiaire_formation_professionnelle = categorie_4 * stagiaire_formation_professionnelle

        categorie_5 = pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_5
        categorie_5_contrat_aide = categorie_5 * contrat_aide

        categories_eligibles = ((pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_1)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_2)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_3)
                                + (categorie_4_stagiaire_formation_professionnelle + categorie_5_contrat_aide))

        #  5
        lieux_activite_eligibles = individu('emploi_ou_formation_en_france', period)

        #  6
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)  # numpy.datetime64
        contrat_de_travail_debut_en_mois = contrat_de_travail_debut.astype('M8[M]')

        date_limite_eligibilite_contrat = min_(
            (contrat_de_travail_debut_en_mois + 1) + (contrat_de_travail_debut - contrat_de_travail_debut_en_mois),
            (contrat_de_travail_debut_en_mois + 2) - np.timedelta64(1, 'D')
            )

        agepi_date_de_demande = individu("agepi_date_demande", period)
        dates_demandes_agepi_eligibles = agepi_date_de_demande <= date_limite_eligibilite_contrat

        #  7
        mayotte = individu.menage('residence_mayotte', period)
        hors_mayotte = not_(mayotte)

        allocation_individu = individu('allocation_retour_emploi', period)

        allocation_minimale_hors_mayotte = parameters(period).allocation_retour_emploi.montant_minimum_hors_mayotte * hors_mayotte
        allocation_minimale_mayotte = parameters(period).allocation_retour_emploi.montant_minimum_mayotte * mayotte

        allocation_minimale_en_fonction_de_la_region = allocation_minimale_hors_mayotte + allocation_minimale_mayotte

        #  Montant ARE minimum en fonction de la région (Mayotte / hors Mayotte)

        are_individu_egale_are_min = np.fabs(allocation_individu - allocation_minimale_en_fonction_de_la_region) < epsilon
        are_individu_inferieure_are_min = allocation_individu < allocation_minimale_en_fonction_de_la_region

        montants_are_eligibles = are_individu_inferieure_are_min + are_individu_egale_are_min

        #  8
        reprises_types_activites = individu('types_activite_condition', period)

        reprises_types_activites_formation = reprises_types_activites == TypesContrat.formation
        reprises_types_activites_cdi = reprises_types_activites == TypesContrat.cdi
        reprises_types_activites_cdd = reprises_types_activites == TypesContrat.cdd
        reprises_types_activites_ctt = reprises_types_activites == TypesContrat.ctt

        #  La formation doit être supérieure ou égale à 40 heures
        duree_formation = individu('heures_remunerees_volume', period)
        periode_formation_eligible = duree_formation >= parameters(period).prestations.agepi.duree_de_formation_minimum

        #  Le durée de contrat de l'emploi doit être d'au moins 3 mois
        periode_de_contrat_3_mois_minimum = individu('contrat_de_travail_duree', period) >= 3

        reprises_types_activites_formation_eligible = reprises_types_activites_formation * periode_formation_eligible
        reprises_types_activites_cdd_eligible = reprises_types_activites_cdd * periode_de_contrat_3_mois_minimum
        reprises_types_activites_ctt_eligible = reprises_types_activites_ctt * periode_de_contrat_3_mois_minimum

        types_et_duree_activite_eligible = (reprises_types_activites_formation_eligible
                                            + reprises_types_activites_cdi
                                            + reprises_types_activites_cdd_eligible
                                            + reprises_types_activites_ctt_eligible)

        eligible_agepi = (parents_isoles
            * condition_nb_enfants
            * agepi_non_percues
            * categories_eligibles
            * lieux_activite_eligibles
            * dates_demandes_agepi_eligibles
            * montants_are_eligibles
            * types_et_duree_activite_eligible)

        return eligible_agepi


class agepi_hors_mayotte(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI - Cas HORS MAYOTTE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20",
        "2. Aide à la garde d’enfants pour les parents isolés (AGEPI)"
        ]

    def formula(individu, period, parameters):
        est_parent = individu.has_role(Famille.PARENT)
        intensite_activite = individu('types_intensite_activite', period)
        nb_heures_semaine = individu('agepi_temps_travail_semaine', period)
        nb_heures_mensuelles = individu('heures_remunerees_volume', period)
        nb_enfants_eligibles = individu.famille('pe_nbenf', period)
        eligibilite_agepi = individu('agepi_eligible', period)

        intensite_hebdomadaire = intensite_activite == TypesIntensiteActivite.hebdomadaire
        intensite_mensuelle = intensite_activite == TypesIntensiteActivite.mensuelle

        hors_mayotte = not_(individu.menage('residence_mayotte', period))

        parametres_montants = parameters(period).prestations.agepi.montants.hors_mayotte
        montants_min_hors_mayotte = parametres_montants.minimum.calc(nb_enfants_eligibles)
        montants_max_hors_mayotte = parametres_montants.maximum.calc(nb_enfants_eligibles)

        montants_min_intensite = montants_min_hors_mayotte * (intensite_hebdomadaire + intensite_mensuelle)
        montants_max_intensite = montants_max_hors_mayotte * (intensite_hebdomadaire + intensite_mensuelle)

        condition_montants_min = ((nb_heures_semaine < 15) * intensite_hebdomadaire) + ((nb_heures_mensuelles < 64) * intensite_mensuelle)
        condition_montants_max = ((nb_heures_semaine >= 15) * intensite_hebdomadaire) + ((nb_heures_mensuelles >= 64) * intensite_mensuelle)

        montant_avec_intensite = (condition_montants_min * montants_min_intensite) + (condition_montants_max * montants_max_intensite)

        montants = hors_mayotte * (est_parent * montant_avec_intensite)

        return eligibilite_agepi * montants


class agepi_mayotte(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI - Cas MAYOTTE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20",
        "2. Aide à la garde d’enfants pour les parents isolés (AGEPI)",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-dg-n2014-48-du-6-jui.html?type=dossiers/2014/bope-n2014-62-du-18-juin-2014",
        ]

    def formula(individu, period, parameters):
        est_parent = individu.has_role(Famille.PARENT)
        intensite_activite = individu('types_intensite_activite', period)
        nb_heures_semaine = individu('agepi_temps_travail_semaine', period)
        nb_heures_mensuelles = individu('heures_remunerees_volume', period)
        nb_enfants_eligibles = individu.famille('pe_nbenf', period)
        eligibilite_agepi = individu('agepi_eligible', period)

        intensite_hebdomadaire = intensite_activite == TypesIntensiteActivite.hebdomadaire
        intensite_mensuelle = intensite_activite == TypesIntensiteActivite.mensuelle

        mayotte = individu.menage('residence_mayotte', period)

        parametres_montants = parameters(period).prestations.agepi.montants.mayotte
        montants_min_mayotte = parametres_montants.minimum.calc(nb_enfants_eligibles)
        montants_max_mayotte = parametres_montants.maximum.calc(nb_enfants_eligibles)

        montants_min_intensite = montants_min_mayotte * (intensite_hebdomadaire + intensite_mensuelle)
        montants_max_intensite = montants_max_mayotte * (intensite_hebdomadaire + intensite_mensuelle)

        condition_montants_min = ((nb_heures_semaine < 15) * intensite_hebdomadaire) + ((nb_heures_mensuelles < 64) * intensite_mensuelle)
        condition_montants_max = ((nb_heures_semaine >= 15) * intensite_hebdomadaire) + ((nb_heures_mensuelles >= 64) * intensite_mensuelle)

        montant_avec_intensite = (condition_montants_min * montants_min_intensite) + (condition_montants_max * montants_max_intensite)

        montants = mayotte * (est_parent * montant_avec_intensite)

        return eligibilite_agepi * montants


class agepi(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20",
        "2. Aide à la garde d’enfants pour les parents isolés (AGEPI)",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-dg-n2014-48-du-6-jui.html?type=dossiers/2014/bope-n2014-62-du-18-juin-2014",
        ]

    def formula(individu, period, parameters):

        agepi_mayotte = ('agepi_mayotte', period)
        agepi_hors_mayotte = ('agepi_hors_mayotte', period)

        return agepi_hors_mayotte + agepi_mayotte