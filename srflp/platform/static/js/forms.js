// Ez csak azert van mert oriasi callback hell-eket okozna par confirm form configja
// eslint-disable-next-line no-unused-vars
const getDeleteScheduleForm = (row) => ({
  title: 'Warning!',
  content: `You are about to delete  Schedule nr. ${row.id}. Do you wish to proceed?`,
  buttons: {
    confirm() {
      $.ajax({
        type: 'post',
        dataType: 'json',
        url: '/schedules/delete',
        data: {
          id: row.id,
        },
        success() {
          $.alert({
            title: 'Success',
            content: `Schedule ${row.id} deleted.`,
          });
          row.remove();
        },
        error(data) {
          console.log(data);
          $.alert({
            title: 'Error',
            content: `Schedule ${row.id} could not be deleted.`,
          });
        },
      });
    },
    cancel() {
    },
  },
});
