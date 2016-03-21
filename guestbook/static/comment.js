var comments = function() {
    this.page_id = pageId;
    this.data = [];
    this.commentBox = $('#commentList')
    var html = '<div class="comment">\
                    <a class="avatar">\
                        <img src="/static/elliot.jpg">\
                    </a>\
                    <div class="content">\
                        <a class="author">{0}</a>\
                        <div class="metadata">\
                            <div class="date">{1}</div>\
                        </div>\
                        <div class="text">{2}</div>\
                    </div>\
                </div>'

    this.render = function() {
        var content = '';
        for (i in this.data) {
            var item = html.format(
                this.data[i].user,
                this.data[i].time,
                this.data[i].text
            );
            content += item;
        }
        this.commentBox.html(content)
    }
    
    this.update = function() {
        var temp;
        $.ajax({
            url : 'comment',
            type: 'GET',
            async: false,
            dataType: 'json',
            data: {board_id: this.page_id},
            success: function (data) {
                console.log(data)
                temp = data.data;
            },
            error: function (jXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        })
        this.data = temp;
    }
    this.updateAll = function() {
        this.update()
        this.render()
    }
}

$(document).ready(function() {
    
    $('#addCommentForm').on('submit', function(e) {
        e.preventDefault();
        console.log($('#sendCommentInput').val())
        $.ajax({
            url: 'comment',
            type: 'POST',
            dataType: 'json',
            data: {
                board_id: pageId, 
                text: $('#sendCommentInput').val()
            },
            success: function (data) {
                com.updateAll()
            },
            error: function (jXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        }).done(function() {
            $('#sendCommentInput').val('')
        })
    })

    com = new comments()
    com.update()
    com.render() 
})

