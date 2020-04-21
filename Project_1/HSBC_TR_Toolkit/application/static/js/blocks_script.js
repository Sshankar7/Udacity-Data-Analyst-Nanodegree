$(document).ready(function () {
    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
      });
    $('input:radio').click(function() {
        if ($("#sel-week-mon1").prop("checked")) {$("#crdiv-rep").addClass("d-none");}
        else {$("#crdiv-rep").removeClass("d-none");} });


    $.validator.addMethod( "extension", function( value, element, param ) {
        param = typeof param === "string" ? param.replace( /,/g, "|" ) : "png|jpe?g|gif";
        return this.optional( element ) || value.match( new RegExp( "\\.(" + param + ")$", "i" ) );
    }, $.validator.format( "Please select file with a valid extension." ) );

    // Select Path Form
    $("#upload_paths_form").validate({
        rules: {
            path_file: {
                required: true,
                extension: 'csv'
            },
        },
        messages: {
            path_file: {
                required: "Please provide a .csv file.",
                extension: "Plese select file with a .csv extension only.",
              },
        },
        submitHandler: function (form) {
            var $form_data = new FormData($('#upload_paths_form')[0]);
            $.ajax({
                url: "/upload_file",
                type: "post",
                data: $form_data,
                processData: false,
                contentType: false,
                success: postEventActivity,
                error: postEventActivity
            });
            return false; // required to block normal submit since you used ajax
        }
    });
    // MI-Info Form
    $("#mi_info_form").validate({
        rules: {
            sel_week_mon: {
                required: true,
            },
            otc_exp_cob: {
                required: true
            },
            otc_sensi_cob: {
                required: true
            },
            exp_stavros_cob: {
                required: true
            },
            sensi_stavros_cob: {
                required: true
            },
            prev_sensi_cob: {
                required: true
            },
        },
        submitHandler: function (form) {
            var $form_data = new FormData($('#mi_info_form')[0]);
            $.ajax({
                url: "/mi_info_process",
                type: "post",
                data: $form_data,
                processData: false,
                contentType: false,
                success: postEventActivity,
                error: postEventActivity
            });
            return false; // required to block normal submit since you used ajax
        }
    });

    // Start Form
    $("#start_form").validate({
        rules: {
            site_select: {
                required: true,
            },
            scenarios_select: {
                required: true
            },
            risk_factor_select: {
                required: true
            },
        },
        submitHandler: function (form) {
            var $form_data = new FormData($('#start_form')[0]);
            $.ajax({
                url: "/start_process",
                type: "post",
                data: $form_data,
                processData: false,
                contentType: false,
                success: postEventActivity,
                error: postEventActivity
            });
            return false; // required to block normal submit since you used ajax
        }
    });

});



function postEventActivity(response) {
    if (response != "Error") {
    if (response == "Upload Success") {$type = "success"; $icon = "fa fa-check mr-5"; $message = "File uploaded successfully!";}
    else if (response == "Upload Error") {$type = "danger"; $icon = "fa fa-times mr-5"; $message = "Oops! Failed to upload file.";}
    else if (response == "MI Success") {$type = "success"; $icon = "fa fa-check mr-5"; $message = "MI Info has been set."}
    else if (response == "MI Error") {$type = "danger"; $icon = "fa fa-times mr-5"; $message = "Oops! Error in setting MI Info."}
    else if (response == "Start Success") {$type = "success"; $icon = "fa fa-check mr-5"; $message = "Process has completed successfully."}
    else if (response == "Start Error") {$type = "danger"; $icon = "fa fa-times mr-5"; $message = "Oops! Error occurred in start process."}
    else if (response == "MIInfo Not Set") {$type = "danger"; $icon = "fa fa-times mr-5"; $message = "MI Info hasn't been set! Kindly set the MI Info before proceeding."}

        Codebase.helpers('notify', {
            align: 'right',
            from: 'top',
            type: $type,
            icon: $icon,
            message: $message
        });
    } else {
        Codebase.helpers('notify', {
            align: 'right',
            from: 'top',
            type: 'danger',
            icon: 'fa fa-times mr-5',
            message: 'Oops! An error has occured.'
        });
    }

}

function blockToggle(showId, hideIds) {
    var hideIds = hideIds.split(" ");
    var i;
    for (i = 0; i < hideIds.length; i++) {
        Codebase.blocks(hideIds[i], 'close');
    }
    Codebase.blocks(showId, 'block_toggle');
}
jQuery(function(){ if ($("#upPaths")) {$("#upPaths").removeClass("d-none");} });

function getProgress() {
    var source = new EventSource("/progress");
	source.onmessage = function(event) {
        console.log(event.data);
        var resData = JSON.parse(event.data);
        if(resData.msg == 'No Data' && resData.pct == '0'){
            source.close()
        }
        else {
            $('.progress-bar').css('width', resData.pct+'%').attr('aria-valuenow', resData.pct);
            $('.progress-bar-label').text(resData.pct+'%');
            $('.elapsed_time').text(resData.elapsed_time+' Minutes');

            if(resData.pct == '100'){
                source.close()
            }
        }
	}
  }