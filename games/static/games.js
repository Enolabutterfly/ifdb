(function($){

    $.widget("crem.authors", {
        options: {
            categoriesUrl: "/json/authors",
            roles: [],
            authors: [],
            value: [],
            authorToId: {},
            idToAuthor: {},
            authorList: [],
        },
        _create: function() {
            var self = this;
            $.getJSON(this.options.categoriesUrl, function(data) {
                $.extend(self.options, data);
                self._build();
            });
        },
        _build: function() {
            var self = this;

            for (var i = 0; i < self.options.authors.length; ++i) {
                var a = self.options.authors[i];
                self.options.authorToId[a['name']] = a['id'];
                self.options.idToAuthor[a['id']] = a['name'];
                self.options.authorList.push(a['name']);
            }

            var createRoleList = function(id) {
                var res = $('<select class="dropdown">blah</select>');
                for (var i = 0; i < self.options.roles.length; ++i) {
                    var role = self.options.roles[i];
                    var option = $('<option/>')
                        .val(role['id'])
                        .text(role['title']);
                    if (role['id'] == id) {
                        option.attr('selected', 'selected');
                    }
                    option.appendTo(res);
                }
                return res;
            }

            var createAuthorInput = function(name) {
                var res = $('<input class="suggest"/>');
                res.val(name);
                res.autocomplete({source: self.options.authorList});
                return res;
            }

            var vals = this.options.value;
            for (var i = 0; i < vals.length; ++i) {
                var entry = $('<div class="entry"></div>');
                var role = createRoleList(vals[i]['role']);
                var author = createAuthorInput(
                    self.options.idToAuthor[vals[i]['author']]);
                var delicon = $('<span class="delicon">&#10006;</span>')
                role.appendTo(entry);
                author.appendTo(entry);
                delicon.appendTo(entry);
                entry.appendTo(this.element);
            }
        }
    });

})(jQuery);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue =
                    decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function PostRedirect(url, data) {
    var form = $('<form method="POST" style="display:none;" />');
    form.attr('action', url);
    var input = $('<input type="hidden" name="json"/>');
    input.val(JSON.stringify(data));
    input.appendTo(form);
    $('<input type="hidden" name="csrfmiddlewaretoken"/>')
        .val(getCookie('csrftoken'))
        .appendTo(form);
    form.appendTo(document.body);
    form.submit();
}

function SubmitGameJson() {
    var res = {};
    res['title'] = $("#title").val();
    if (res['title'] == '') {
        $("#title_warning").show();
        return;
    }
    res['description'] = $('#description').val();
    res['release_date'] = $('#release_date').val();
    PostRedirect('/store_game', res);
}