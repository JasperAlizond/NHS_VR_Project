var editor_video_view = null;

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
    var data = editor_video_view.data("tags");
    editor_video_view.html("");
    for (var tag of data){
        w_c = video_coords_to_world_coords(tag.fields.x, tag.fields.y, tag.fields.width, tag.fields.height);
        $("#tag-container").append(`<div class='tag' id="tag-${tag.pk}" data-tag='${JSON.stringify(tag)}' style="top:${w_c.x}px; left:${w_c.y}px;width:${w_c.w}px;height:${w_c.h}px;">${tag.fields.local_content}</div>`);
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

$(window).on("load", () => {
    editor_video_view = $("#editor-video-view");
    var tags = load_tags();
    setInterval(()=>update_visible(tags), 16);
});
