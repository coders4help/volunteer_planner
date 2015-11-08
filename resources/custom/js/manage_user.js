$(function () {


    $('#manageMembership .action').on('click', function () {
        var thiz = $(this)
        var data = {

            "user_account_id": thiz.parents('td').siblings('.manage-member').attr('data-account-id'),
            "facility_id": thiz.parents('td').siblings('.manage-member').attr('data-facitlity-id'),
            "action": thiz.attr('data-action')

        }
        ajaxPost('/orgs/manage_ajax/', data, function (content) {
            //onSuccess
            alert(content);
        })

        console.log(data)
    })

});