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

// function changeDisplay() {
//     let checkBox = document.getElementsByName('checkbox')
//     var Arr = []
//
//     for (var i = 0; i < checkBox.length; i++) {
//         if (checkBox[i].checked === true) {
//             document.getElementById('trash').style.display = 'flex'}
//         else
//             document.getElementById('trash').style.display = 'none'
//
//     }
// }

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

