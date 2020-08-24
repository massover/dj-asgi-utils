const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const evtSource = new EventSource("/api/v1/toast/stream/");
let ids = [];
console.log("HELLO WORLD!!");
const notyf = new Notyf({duration: 0, dismissible: true});
evtSource.addEventListener("toast", function (event) {
  const toasts = JSON.parse(event.data);
  toasts.forEach(toast => {
    if (ids.includes(toast.id)) {
      return
    }
    ids.push(toast.id);
    const notification = notyf.success(toast.message);
    notification.on('dismiss', ({target, event}) => {
      // target: the notification being clicked
      // event: the mouseevent
      const request = new Request(
        `/api/v1/toast/${toast.id}/read/`,
        {headers: {'X-CSRFToken': csrftoken}}
      );
      ids = ids.filter(id => id !== toast.id);
      fetch(request, {method: 'POST'});
    });
  })
});