
$(document).ready(function() {

    // desactivation des choix
    $('#region_origine').attr('disabled', 'disabled')
    $('#departement_origine_id').attr('disabled', 'disabled')


    // fonctions de mise a jour des regions
    function updateRegions(choice) {
        var propagate = false;
        var correctOptions = $('#region_origine option[value^="' + choice + '"]');
        var incorrectOptions = $('#region_origine option:not([value^="' + choice + '"])');
        var choiceOption = $('#region_origine option[value=""]');
        var field = $('#region_origine');
        
        field.val('');
        if (correctOptions.length == 0 )  {
            field.attr('disabled', 'disabled');
        } else if (correctOptions.length == 1 ) {
            field.val(correctOptions.attr('value'))
            incorrectOptions.hide();
            correctOptions.hide();
            choiceOption.hide();
            field.removeAttr('disabled');
            propagate = true
        } else {
            incorrectOptions.hide();
            correctOptions.show();
            choiceOption.show();
            field.removeAttr('disabled');
        }
        return propagate;
    }

    // fonctions de mise a jour des regions
    function updateDepartements(choice) {
        var correctOptions = $('#departement_origine_id option[value^="' + choice + '"]');
        var incorrectOptions = $('#departement_origine_id option:not([value^="' + choice + '"])');
        var choiceOption = $('#departement_origine_id option[value=""]');
        var field = $('#departement_origine_id');
        
        field.val('');
        if (correctOptions.length == 0 )  {
            field.attr('disabled', 'disabled');
        } else if (correctOptions.length == 1 ) {
            field.val(correctOptions.attr('value'))
            incorrectOptions.hide();
            correctOptions.hide();
            choiceOption.hide();
            field.removeAttr('disabled');
        } else {
            incorrectOptions.hide();
            correctOptions.show();
            choiceOption.show();
            field.removeAttr('disabled');
        }
    }

    // precedures evenementielles
    $('#nationalite').change(function () {
        choice = $(this).val();
        var propagate = updateRegions(choice);
        if (propagate) {
            updateDepartements(choice);
        } else {
            updateDepartements('');
        }
    })

    $('#region_origine').change(function () {
        choice = $(this).val();
        updateDepartements(choice);
    })
    
});