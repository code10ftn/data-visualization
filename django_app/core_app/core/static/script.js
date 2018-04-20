function submitLoadDataForm(plugin_id) {
    document.getElementById('plugin_id').value = plugin_id;
    document.forms["load_data"].submit();
}

function raiseError(msg) {
    if (msg !== "") {
        alert(msg);
    }
}