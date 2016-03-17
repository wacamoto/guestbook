if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : ''
      ;
    });
  };
}

$(document).ready(function() {
    var comments = function() {
        this.page_id = pageId;
        this.data = [{name:'name1', time:'time1', text:'text1'},{name:'name1', time:'time1', text:'text1'},{name:'name1', time:'time1', text:'text1'}];
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
                    this.data[i].name,
                    this.data[i].time,
                    this.data[i].text
                );
                content += item;
            }
            this.commentBox.html(content)
        }
        
        this.update = function() {
            $.ajax({
                url : 'getcomment',
                type: 'GET',
                dataType: 'json',
                data: {board_id: this.page_id},
                success: function (data) {
                    console.log(data)
                    this.data = data
                },
                error: function (jXHR, textStatus, errorThrown) {
                    alert(errorThrown);
                }
            });
        }
    }

    $('#addCommentForm').on('submit', function(e) {
        e.preventDefault();

        console.log($('#sendCommentInput').val())
        $.ajax({
            url: 'addcomment',
            type: 'GET',
            dataType: 'json',
            data: {
                board_id: pageId, 
                mesg: $('#sendCommentInput').val()
            },
            success: function (data) {
                console.log(data)
                this.data = data
            },
            error: function (jXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        })
    })


    com = new comments()
    com.render()    
})

