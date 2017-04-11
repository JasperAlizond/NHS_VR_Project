var editor_video_view = null;
var current_tag = null;
var active_drag_node = null;
var resize_mode = -1;

function update_tag_form() {
    if (current_tag === null) {
        $("#current-tag label").hide();
        $("#current-tag > button").hide();
        $("#current-tag > h3").text("No current selected tag");
    } else {
        $("#current-tag > h3").text("Current Tag");
        $("#current-tag label").show();
        $("#current-tag > button").show();
        $("input[name=x]").val(current_tag.fields.x);
        $("input[name=y]").val(current_tag.fields.y);
        $("input[name=width]").val(current_tag.fields.width);
        $("input[name=height]").val(current_tag.fields.height);
        $("input[name=time-start]").val(current_tag.fields.time_start);
        $("input[name=time-end]").val(current_tag.fields.time_end);
        if(current_tag.fields.remote){
            $("#local-label").hide();
            $("input[name=remote-url]").val(current_tag.fields.remote_url);
        } else{
            $("#remote-label").hide();
            $("textarea[name=local-content]").val(current_tag.fields.local_content);
        }
    }
}

function video_coords_to_world_coords(v_x, v_y, v_w, v_h) {
    var scale_x = editor_video_view[0].scrollWidth / editor_video_view[0].videoWidth;
    var scale_y = editor_video_view[0].scrollHeight / editor_video_view[0].videoHeight;
    
    return {
        x: v_x * scale_x,
        y: v_y * scale_y,
        w: v_w * scale_x,
        h: v_h * scale_y
    }
}

function load_tags() {
    $(".tag").remove();
    var data = editor_video_view.data("tags");
    editor_video_view.html("");
    for (var tag of data){
        if (tag.deleted === true) continue;

        var w_c = video_coords_to_world_coords(tag.fields.x, tag.fields.y, tag.fields.width, tag.fields.height);

        if (tag.fields.remote === false){
            $("#tag-container").append(`<div class='tag' id="tag-${tag.pk}" data-tag='${JSON.stringify(tag)}' style="top:${w_c.y}px; left:${w_c.x}px;width:${w_c.w}px;height:${w_c.h}px;">${tag.fields.local_content}</div>`);
        } else{
            $("#tag-container").append(`<div class='tag' id="tag-${tag.pk}" data-tag='${JSON.stringify(tag)}' style="top:${w_c.y}px; left:${w_c.x}px;width:${w_c.w}px;height:${w_c.h}px"><img src="${'https://' + new URL('https://'+tag.fields.remote_url).host + '/favicon.ico'}"></img> This is a remote link to ${tag.fields.remote_url}</div>`);
        }

        var tag_elem = $(`#tag-${tag.pk}`);
        tag_elem.on("mouseover", function(e){
            current_tag = $(e.target).data("tag");
            update_tag_form();
        });
        tag_elem.mousedown(function(e){
            if(e.which === 1 && confirm("Are you sure you want to delete this tag?")){
                var data = editor_video_view.data("tags");
                for (var i = 0; i < data.length; i++) {
                    if (data[i].pk === $(e.target).data("tag").pk){
                        data[i].deleted = true;
                    }
                }
                editor_video_view.attr("data-tags", JSON.stringify(data));
                load_tags();
            }
        });
    }
}

function update_visible(tags) {
    $(".tag").each(function(index, element){
        var data = $(element).data("tag");
        var current_time = editor_video_view[0].currentTime
        var visible = current_time > data.fields.time_start && current_time < data.fields.time_end;
        $(element).toggle(visible);
    });
}

function createTag(remote){
    var data = editor_video_view.data("tags");
    data.push(
        {"model": "tagger.tag",
             "pk": Math.floor(Math.random() * 1000000 + 1000),
             "fields": {
                "video": editor_video_view.data("video-id"),
                "x": 50,
                "y": 50,
                "width": 500,
                "height": 500,
                "time_start": Math.floor(editor_video_view[0].currentTime),
                "time_end": Math.floor(editor_video_view[0].currentTime + 10),
                "remote": remote,
                "local_content": "Insert Text Content Here",
                "remote_url": "https://www.google.com"
             }
        }
    );
    editor_video_view.attr("data-tags", JSON.stringify(data));
    load_tags();
}

$(window).on("load", () => {
    editor_video_view = $("#editor-video-view");
    var tags = load_tags();
    update_tag_form();
    $("#update-tag").click(function(e){
        current_tag.fields.x = $("input[name=x]").val();
        current_tag.fields.y = $("input[name=y]").val();
        current_tag.fields.width = $("input[name=width]").val();
        current_tag.fields.height = $("input[name=height]").val();
        current_tag.fields.time_start = parseInt($("input[name=time-start]").val());
        current_tag.fields.time_end = parseInt($("input[name=time-end]").val());
        current_tag.fields.remote_url = $("input[name=remote-url]").val();
        current_tag.fields.local_content = $("textarea[name=local-content]").val();
        var data = editor_video_view.data("tags");
        for (var i = 0; i < data.length; i++) {
            if (data[i].pk === current_tag.pk){
                data[i] = current_tag;
            }
        }
        editor_video_view.attr("data-tags", JSON.stringify(data));
        load_tags();
    });
    
    $("#create-text-tag").click((e)=>createTag(false));
    $("#create-remote-tag").click((e)=>createTag(true));

    $("#save-tags").click(function(e){
        var tags = editor_video_view.data("tags");
        $.ajax(window.location.pathname, {
            data: JSON.stringify(tags),
            beforeSend: function(request){
                request.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            },
            contentType: 'application/json',
            type: 'POST'
        });
    });
    setInterval(()=>update_visible(tags), 16);
});
