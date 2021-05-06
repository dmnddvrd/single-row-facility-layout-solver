const validateHour = () => {
  const hour = parseInt($('#hour').val(), 10);
  const btn = $('#schedule-create-btn');
  if (Number.isNaN(hour) || (hour > 24 || hour < 0)) {
    $('#hour').addClass('incorrect');
    btn.addClass('disabled');
    btn.prop('disabled', true);
    return false;
  }
  $('#hour').removeClass('incorrect');
  btn.removeClass('disabled');
  btn.prop('disabled', false);
  return true;
};

const validatePrice = () => {
  const price = parseInt($('#price').val(), 10);
  const btn = $('#schedule-create-btn');
  if (Number.isNaN(price) || price < 0) {
    $('#price').addClass('incorrect');
    btn.addClass('disabled');
    btn.prop('disabled', true);
    return false;
  }
  $('#price').removeClass('incorrect');
  btn.removeClass('disabled');
  btn.prop('disabled', false);
  return true;
};

const deleteSchedule = (row) => {
  // eslint-disable-next-line no-undef
  $.confirm(getDeleteScheduleForm(row));
};

const createSchedule = (schedule) => {
  $.confirm({
    title: 'Confirmation',
    content: `You are about to create the following schedule:<br> ${schedule.from} => ${schedule.to} 
    (${schedule.days}-${schedule.hour}:00) ${schedule.price} RON`,
    buttons: {
      confirm() {
        $.ajax({
          type: 'post',
          dataType: 'json',
          url: '/schedules/create',
          data: schedule,
          success(response) {
            console.log(response);
            const id = response.scheduleId[0];
            $.alert({
              title: 'Success',
              content: `Schedule ${id} created.`,
            });
            $('#schedules-table').append(`
            <tr class="schedule" id="${id}">
              <td>${id}</td>
              <td>${schedule.from}</td>
              <td>${schedule.to}</td>
              <td>${schedule.days}</td>
              <td>${schedule.hour}:00</td>
              <td>${schedule.type}</td>
              <td>${schedule.price} RON</td>
            </tr>`);
            // bug miatt parent-et kell atadjak mert a td-t veszi klikkelt nodusnak nem a tr-t
            $('tr.schedule:last-of-type').click((e) => {
              deleteSchedule(e.target.parentNode);
            });
          },
          error() {
            $.alert({
              title: 'Error',
              content: `Schedule ${schedule} could not be created.`,
            });
          },
        });
      },
      cancel() {
      },
    },
  });
};

$(document).ready(() => {
  $('tr.schedule').click((e) => {
    deleteSchedule(e.target.parentNode);
  });
  $('#hour').blur(validateHour);
  $('#price').blur(validatePrice);
  $('#schedule-create-btn').click(() => {
    if ($('#from').val() && $('#to').val() && $('#frequency').val() && $('#hour').val() && $('#type').val() && $('#price').val()) {
      createSchedule({
        from: $('#from').val(),
        to: $('#to').val(),
        days: $('#frequency').val(),
        hour: $('#hour').val(),
        type: $('#type').val(),
        price: $('#price').val(),
      });
    } else {
      $.alert({
        title: 'Error',
        content: 'Form incomplete or incorrect. Hour must be an integer between 0-24, price can\'t be negative.',
      });
    }
  });
});
