(function() {
	'use strict';

    $('.update-task').on('submit', function(e) {
        var data = Utils.getFormData('.update-task'),
            gm_id = $('#gm_id').val(),
            gm_role = $('#gm_role').val();

        console.log(gm_role);    
        if (gm_role == 'attacker' )
        {
           var url = '/game/attacker/'+gm_id+'/';
        }
        if (gm_role == 'defender')
        {
            var url = '/game/defender/'+gm_id+'/';
        }
        Utils.submitForm(e, data, url);
        return false;
    })
    

})();


