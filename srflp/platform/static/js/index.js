$(function () {
  $("form").submit(function (ev) {
    ev.preventDefault();

    var form = $(this);
    var data = {};

    form.find("input, select, textarea").each(function () {
      data[$(this).attr("name")] = $(this).val();
    });

    var isJson = true;

    try {
      data["srflp_json"] = data["srflp_json"].replace(/\"\"/g, '"');
      JSON.parse(data["srflp_json"]);
    } catch (err) {
      isJson = false;
    }

    if (isJson) {
      $.post({
        url: "/problems/create",
        data: data,
        dataType: "json",
        success(response) {
          console.log(response);
          window.location.reload();
        },
        error(err) {
          console.error(err);
        },
      });
    } else {
      alert("Input value must be a valid JSON!");
    }
  });
});
