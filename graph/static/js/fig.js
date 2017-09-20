function draw(graph){
    var categories = [];
    var ca = graph.categories;

    var graph_title = graph.title;
    console.log('graph_title=' , graph_title)

    for (var i=0; i<ca.length; i++){
        categories[i] = {name: ca[i]};
    }

    console.log('graph = ', graph)

    option = {
        title: {
            text: graph_title,
            top: 'bottom',
            left: 'left'
        },
        tooltip: {
            formatter : '{c}'
        },
        animation: true,
//        backgroundColor: '#f0f0f0',
        legend: [{
            selectedMode: 'single',
            data: categories.map(function (a) {
                return a.name;
            })
        }],
        series : [
            {
                name: '',
                type: 'graph',
                layout: 'force',
                // hoverAnimation: true,
                data: graph.nodes,
                links: graph.links,
                categories: categories,
                focusNodeAdjacency: true,
                draggable: true,
                roam: true,
                force: {

                    repulsion: 50
                }
            }
        ]
    };
    myChart.setOption(option);

    console.log(option);
    myChart.on('click', click_func);
}



function click_func(params) {
    if (params.componentType === 'series') {
        if (params.seriesType === 'graph') {
            if (params.dataType === 'edge') {
                console.log('click edge to move')
                // 点击到了 graph 的 edge（边）上。
            }
            else {
                if(params.data.layer == 3){
                    console.log('click on the layer 3')
                    $('#instruction').remove();
                    var note_area = document.getElementById('note');
                    var note_title = params.data.topword + '-' + params.data.value
                    var note_data = JSON.stringify({'data': params.data.sentenseList,'title': note_title, 'table': true})
                    // var note_data = JSON.stringify({'data': ['中文'], 'title': '测试', 'table': false})
                    // $('#note').load('note #panel-2')
                    // AddHTML()
                    $.post('add_note', note_data, function(ret){
                        $('#note').html(ret);
                    })

                    // $.post("note", function(note_data) {
                    //     $("#note").html(note_data);
                    // });
                    // $('#note').load('note #panel-2', note_data)
                    // var note_html = getHTML();
                    // note_area.innerHTML = note_html(note_data);
                }
                // 点击到了 graph 的 node（节点）上。
            }
        }
    }
}


function AddHTML() {
    var post_data = JSON.stringify({"data": ['hello'], 'title': 'test', 'table': false});

    console.log("post_data", post_data)

    $.ajax({
        url: 'add_note',
        type: "POST",
        data: post_data,
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            // data = JSON.parse(data);
            if (data["status"] == 1) {
                console.log('success!')
                $('#note').innerHTML = data["html"]
            }
        }
    });
} 


function getHTML(data)
{
    var input = document.createElement('div');
    input.setAttribute('div', )

    var html = '<div id="panel-2">\
        <h2>\
            <font face="微软雅黑">{{ title }}</font>\
        </h2>\
        <br/>\
        {% if table %}\
            <table class="table" width="80%">\
                <tbody>\
                {% for item,info in data.items %}\
                <tr>\
                    <td width="30%"><strong>{{ item }}</strong></td>\
                    <td>{{ info }}</td>\
                </tr>\
                {% endfor %}\
                </tbody>\
            </table>\
        {% else %}\
            <p>\
                {% for item in data %}\
                    {% autoescape off %}{{ item }}{% endautoescape %}<br>\
                {% endfor %}\
            </p>\
        {% endif %}\
    </div>';

    return html;
}

function loadPage(href)
{
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", href, false);
    xmlhttp.send();
    return xmlhttp.responseText;
}

// myChart.on('click', function (params) {
// //    var post_data = {'point_click': {'name': params.name, 'value':params.value}};
//     var post_data = {'point_click': params.name, 'point_click_value': params.value, 'point_click_txt': params.data.txt};
//     $.get('search', post_data, function(data){
//            $('#panel-2').html(data);
//     });
// });


// myChart.on('dblclick', function (params) {
// //    var post_data = {'point_click': {'name': params.name, 'value':params.value}};
//     var name = params.name;
//     var value = params.value;
//     var txt = params.data.txt;
//     if (txt==""){
//         window.location.href="search?q="+value;
//     }


// });

$(document).ready(function(){
    draw(graph_d);
});




// $("#search_box").typeahead({
//     source: function(query, process){
//         $.get('search', {'sbox':query}, function(e){
//                 process(e);
//         });
//     },
//     items: 8,
//     updater: function (item) {
//         return item;
//     },
//     displayText: function (item) {
//         return item;
//     },
//     afterSelect: function (item) {
//         window.location.href="search?q="+item;
//     },
//     delay: 200
// });
/*$("#look_up_array").click(function () {
    $("#local_data").typeahead("lookup", '选');
});
$("#get_value_array").click(function () {
    var val = $("#local_data").typeahead("getActive");
    console.log(val);
});*/
