let reservations = [];

const createReservation = (data) => {
  $.ajax('/reservations/create', {
    type: 'post',
    data,
    dataType: 'json',
    success(response) {
      return response;
    },
    error(err) {
      console.log(err);
      return false;
    },
  });
};

const confirmReservationForm = (scheduleData) => {
  let content = '<table style="width:100%" class="reservations-form-table">'
  + '<tr>'
  + ' <th>ID</th>'
  + ' <th>Reservation Note</th>'
  + ' <th>Time</th>'
  + ' </tr>';

  reservations.filter((r) => r.schedule_id === parseInt(scheduleData.id, 10)).forEach((val) => {
    content += `<tr><td>${val.id}</td><td>${val.reservation_for}</td><td>${val.created_at}</td></tr>`;
  });
  content += '</table></form>'
  + '<form action="" class="formName">'
  + '<h1>Creat a reservation:</h1>'
  + '<div class="form-group" style ="display:flex; flex-direction: column;">'
  + ''
  + '<label>Enter a Name for your reservation</label>'
  + `<input type="text" placeholder="${scheduleData.user_name}" class="name form-control" required />`
  + ''
  + '<label>Nr of seats (max:4)</label>'
  + '<input type="number" placeholder="1" min="1" max="4" class="nr_of_seats form-control" required />'
  + ''
  + '</div>';

  $.confirm({
    title: `Reservations for ${scheduleData.from} -> ${scheduleData.to}(${scheduleData.type}) at the Price of ${scheduleData.price}`,
    content,
    buttons: {
      formSubmit: {
        text: 'Submit',
        btnClass: 'btn-blue',
        action() {
          const copy = scheduleData;
          copy.reservation_for = this.$content.find('.name').val();
          copy.nr_of_seats = this.$content.find('.nr_of_seats').val();
          copy.schedule_id = copy.id;
          console.log(copy);
          createReservation(copy);
          $.ajax('/reservations/all', {
            type: 'get',
            dataType: 'json',
            success(response) {
              reservations = response.reservations;
              console.log(reservations);
            },
            error(err) {
              console.log(err);
              return false;
            },
          });
        },
      },
      cancel() {
      },
    },
  });
};


$(document).ready(() => {
  $('#schedule-btn').click(() => {
    $.ajax('/schedules/all', {
      type: 'get',
      data: {
        from: $('#from').val() === '' ? undefined : $('#from').val(),
        to: $('#to').val() === '' ? undefined : $('#to').val(),
        // TODO: come up with better solution
        minPrice: $('#minPrice').val() === '' ? 0 : $('#minPrice').val(),
        maxPrice: $('#maxPrice').val() === '' ? 99999 : $('#maxPrice').val(),
      },
      dataType: 'json',
      success(data) {
        const timetable = data.schedules;
        $('.schedule').remove();
        timetable.forEach((item) => {
          if (item) {
            $('#schedules-table').append(`
            <tr class="schedule">
              <td>${item.id}</td>
              <td>${item.from}</td>
              <td>${item.to}</td>
              <td>${item.days}</td>
              <td>${item.hour}:00</td>
              <td>${item.type}</td>
              <td>${item.price} RON</td>
            </tr>`);
          }
        });
        $('#schedules-table')
          .fadeOut(100)
          .fadeIn(100);
      },
      error(err) {
        console.log(err);
      },
    });
  });
  $('tr.schedule').click((e) => {
    let scheduleData = {};
    const clickedRow = e.target.parentNode.cells;
    scheduleData = {
      id: clickedRow[0].innerHTML,
      user_name: 'Edi',
      user_id: 1,
      from: clickedRow[1].innerHTML,
      to: clickedRow[2].innerHTML,
      hour: clickedRow[3].innerHTML,
    };
    let schedule = {};
    $.ajax('/schedules/all', {
      type: 'get',
      dataType: 'json',
      success(response) {
        const schedules = Object.values(response.schedules);
        schedule = schedules.filter((elem) => elem.id === parseInt(scheduleData.id, 10));
        // updating the selected schedule's price
        scheduleData.price = schedule[0].price;
        scheduleData.type = schedule[0].type;
        confirmReservationForm(scheduleData);
      },
      error(err) {
        console.log(err);
        return false;
      },
    });
  });
  $.ajax('/reservations/all', {
    type: 'get',
    dataType: 'json',
    success(response) {
      reservations = response.reservations;
      console.log(reservations);
    },
    error(err) {
      console.log(err);
      return false;
    },
  });
});
