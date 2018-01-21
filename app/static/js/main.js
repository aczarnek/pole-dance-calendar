$(document).ready(function() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month'
        },
        defaultDate: Date.now(),
        firstDay: 1,
        editable: false,
        eventLimit: true,
        navLinks: true,
        events: {
            url: 'data',
            error: function() {
                $('#script-warning').show();
            }
        },
        eventClick: function(calEvent, jsEvent, view) {

        var cal_modal = $("div.modal:first").clone();
                            cal_modal.attr('id', calEvent.id);
                        cal_modal.find('div.modal-header').removeClass().addClass('modal-header')
                        cal_modal.find('div.modal-header').addClass(calEvent.className[0]);
                        cal_modal.find('h5').empty().append(calEvent.className);
                        cal_modal.find('h2').empty().append(calEvent.title);
                        cal_modal.find('h4').empty().append(calEvent.start.format('YYYY-MM-DD HH:mm'), ' ', calEvent.organizer);
                        cal_modal.find('p.modal-description').empty().append(calEvent.description.replace(/\n/g, "<br />"));
                        cal_modal.find('p.modal-organizer').empty().append(calEvent.organizer);
                        cal_modal.find('span.address').empty()
                        .append(calEvent.al1, '</br>', calEvent.city, ' ', calEvent.al2);

        $(this).attr('dataTarget', calEvent.id).attr('data-toggle', 'modal');

////        // change the border color
//        $(this).css('border-color', 'red');

        cal_modal.insertAfter(".user-events-list");
        var cal_id = '#' + cal_modal.attr('id');
        $(cal_id).modal('show');
    },
        loading: function(bool) {
            $('#loading').toggle(bool);
        }
    });

    $(function() {
        $('#submit').click(function(){

        $('#user-events-list').empty();

        var type = $('input[type="checkbox"]:checked');
        var city = $('select').val();

        $.ajax({
            url: '/events',
            type: 'POST',
            data: $( "form" ).serialize(),
            dataType: 'json',
            })

            .done(function(data) {

            if (data.type_error) {
                $('#cityAlert').hide();
                $('#emptyAlert').hide();
                $('#typeAlert').text(data.type_error).show();
            }

            else if (data.city_error) {
                $('#emptyAlert').hide();
                $('#typeAlert').hide();
                $('#cityAlert').text(data.city_error).show();
            }

            else if (data.empty_error) {
                $('#cityAlert').hide();
                $('#typeAlert').hide();
                $('#emptyAlert').text(data.empty_error).show();
            }

            else {
                    $('#typeAlert').hide();
                    $('#emptyAlert').hide();
                    $('#cityAlert').hide();

// Variable which create li element with appropriate elements for modal, but it not working :(

                    var li=$('<li>')
                        .attr({class: 'user_event', 'data-toggle': 'modal' })
                        .append($('<h5>'), $('<h4>'), $('<span>')
                            .attr('class', 'pd-event-who2'));

                    var event = '';
                    $.each(data[0], function(index, value) {

                    var stringId = value.Id.toString();
                    var nameId = '#event-details';
                    var nameId2 = 'event-details'
                    var dataTarget = nameId + stringId;
                    var eventDetails = nameId2 + stringId;

                        event = $(li).clone();

                        $(event).attr('data-target', dataTarget);
                        $(event).find('h5').append(value.Start.replace('T', ' '), ' ', value.City);
                        $(event).find('h4').append(value.Name);
                        $(event).find('span').append(value.Organizer);


                        var modal = $("div.modal:first").clone();
                        modal.attr('id', eventDetails);
                        modal.find('div.modal-header').removeClass().addClass('modal-header').addClass(value.Type);
                        modal.find('div.value.Type').addClass('modal-header');
                        modal.find('h5').empty().append(value.Type);
                        modal.find('h2').empty().append(value.Name);
                        modal.find('h4').empty().append(value.Start.replace('T', ' '), ' ', value.Organizer);
                        modal.find('p.modal-description').empty().append(value.Description.replace(/\n/g, "<br />"));
                        modal.find('p.modal-organizer').empty().append(value.Organizer);
                        modal.find('span.address').empty()
                        .append(value.AddressLine1, '</br>', value.City, ' ', value.AddressLine2);
                        $('.user-events-list').append(event);
                        modal.insertAfter(event);
                    });
                    }
                });

            event.preventDefault();

    //
    //        },
    //        error: function(error) {
    //            console.log(error);
    //        }

        });
    });

    $("div[id^='event-details']").on("shown.bs.modal", function(e){
        google.maps.event.trigger(map, "resize");

    });
});
