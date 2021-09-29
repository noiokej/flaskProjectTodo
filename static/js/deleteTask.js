var $ = jQuery;

$(function() {
  $('#content').focus();
});

function change(list) {
    document.getElementById('hidd').value = list

}

function deleteCheckedTask() {
    let checkBox = document.getElementsByName('checkbox')
    console.log(checkBox)
    var arrTasksToDelete = []

    for (var i = 0; i < checkBox.length; i++) {
        if (checkBox[i].checked === true) {
            checked = Array.from(checkBox)
            console.log(checked)
            arrTasksToDelete.push(checked[i].value)
        }
    }

    document.getElementById('delete').value = arrTasksToDelete
    console.log(arrTasksToDelete)
    return arrTasksToDelete
}

function changeDisplay(taskId) {

    id = document.getElementById(`task-${taskId}`)
    var Arr = []
    let checkBox = document.getElementsByName('checkbox');


    function lastClick() {
        console.log(id.checked)
        id.checked === false ? document.getElementById('trash').style.display = 'flex'
            : Arr.length <= 1 ? document.getElementById('trash').style.display = 'none' :
        console.log(id.checked)
    }

    function allChecked() {
        for (var i = 0; i < checkBox.length; i++) {
            if (checkBox[i].checked === true ) {
                Arr.push(i)
            }
        }
        return Arr
    }

    lastClick(allChecked())
    console.log(Arr)
}

// var data = {"name":"John Doe","age":"21"}
// // function deleteTask() {
// $.ajax({
//     type: "POST",
//     // url: '/' + id + '/delete',
//     // url: "http://localhost:5000/",
//     url: "http://localhost:5000/",
//     contentType: "application/json",
//     // data: JSON.stringify(data),
//     data: data,
//     dataType: "json",
//     success: [function(response) {
//         console.log(response);
//     }],
//     error: [function (err) {
//         console.log(err);
//     }]
// })
// }

