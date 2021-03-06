openerp.ob_web_replace = function(instance) {
    var QWeb = instance.web.qweb;
        _t = instance.web._t;
    instance.web.Dialog.include({
        renderElement: function () {
           this._super.apply(this, arguments);
           if (this.dialog_title && typeof(this.dialog_title) == 'string') {
               this.dialog_title = this.dialog_title.replace(/odoo/ig, "");
           }
       }, 
    });
    instance.web.form.AbstractField.include({
        init: function(field_manager, node) {
            var self = this;
            this._super(field_manager, node);
            if (this.node.attrs.placeholder) {
                this.node.attrs.placeholder = this.node.attrs.placeholder.replace(/odoo.com/ig, "");
                this.node.attrs.placeholder = this.node.attrs.placeholder.replace(/odoo/ig, "");
            }
        },
        is_false: function() {
            check_space = /\S|^$/.test(this.get('value'));
            return this.get('value') === false || !check_space ;
        },
    });
    instance.web.ViewManagerAction.include({
        set_title: function (title) {
            this._super.apply(this, arguments);
            newtitle = this.get_action_manager().get_title();
            newtitle = newtitle.replace(/odoo/ig, "");
            this.$el.find('.oe_breadcrumb_title:first').html(newtitle);
        },
    });
    instance.web.WebClient.include({
        init: function(parent, client_options) {
            var self = this;
            this._super(parent, client_options);
            this.set('title_part', {"zopenerp": ""});
        }
    });
    instance.web.ListView.include({
        no_result: function () {
            this.$el.find('.oe_view_nocontent').remove();
            if (this.groups.group_by || !this.options.action || !this.options.action.help) {
                return;
            }
            this.$el.find('table:first').hide();
            title = this.options.action.help.replace(/odoo/ig, "");
            this.$el.prepend(
                $('<div class="oe_view_nocontent">').html(title)
            );
            var create_nocontent = this.$buttons;
            this.$el.find('.oe_view_nocontent').click(function() {
                create_nocontent.openerpBounce();
            });
        },
    });
    instance.web_kanban.KanbanView.include({
        no_result: function () {
            if (this.groups.group_by
                || !this.options.action
                || !this.options.action.help) {
                return;
            }
            this.$el.find('.oe_view_nocontent').remove();
            title = this.options.action.help.replace(/odoo/ig, "");
            this.$el.prepend(
                $('<div class="oe_view_nocontent">').html(title)
            );
            var create_nocontent = this.$buttons;
            this.$el.find('.oe_view_nocontent').click(function() {
                create_nocontent.openerpBounce();
            });
        },
    });

    instance.web.CrashManager.include({
        show_warning: function(error) {
            if (!this.active) {
                return;
            }
            if (error.data.exception_type === "except_osv") {
                error = _.extend({}, error, {data: _.extend({}, error.data, {message: error.data.arguments[0] + "\n\n" + error.data.arguments[1]})});
            }
            new instance.web.Dialog(this, {
                size: 'medium',
                title: "Perceive " + (_.str.capitalize(error.type) || "Warning"),
                buttons: [
                    {text: _t("Ok"), click: function() { this.parents('.modal').modal('hide'); }}
                ],
            }, $('<div>' + QWeb.render('CrashManager.warning', {error: error}) + '</div>')).open();
        },
        show_error: function(error) {
            if (!this.active) {
                return;
            }
            var buttons = {};
            buttons[_t("Ok")] = function() {
                this.parents('.modal').modal('hide');
            };
            new instance.web.Dialog(this, {
                title: "Perceive " + _.str.capitalize(error.type),
                buttons: buttons
            }, QWeb.render('CrashManager.error', {session: instance.session, error: error})).open();
        },
     });
     
     instance.web.DatabaseManager.include({
        
        init: function(parent) {
            this._super(parent);
        },
        
        start: function() {
            var self = this;
            
            $('.oe_secondary_menus_container,.oe_user_menu_placeholder').empty();
            var fetch_db = this.rpc("/web/database/get_list", {}).then(
                function(result) {
                    self.db_list = result;
                },
                function (_, ev) {
                    ev.preventDefault();
                    self.db_list = null;
                });
            var fetch_langs = this.rpc("/web/session/get_lang_list", {}).done(function(result) {
                self.lang_list = result;
            });
            return $.when(fetch_db, fetch_langs).always(self.do_render);
        },
        do_render: function() {
            var self = this;
            instance.webclient.toggle_bars(true);
            self.$el.html(QWeb.render("DatabaseManager", { widget : self }));
            var text = self.$el.html();
            
            text = text.replace(/Odoo/ig, "");
            self.$el.html(text);
            $('.oe_user_menu_placeholder').append(QWeb.render("DatabaseManager.user_menu",{ widget : self }));
            $('.oe_secondary_menus_container').append(QWeb.render("DatabaseManager.menu",{ widget : self }));
            $('ul.oe_secondary_submenu > li:first').addClass('active');
            $('ul.oe_secondary_submenu > li').bind('click', function (event) {
                var menuitem = $(this);
                menuitem.addClass('active').siblings().removeClass('active');
                var form_id =menuitem.find('a').attr('href');
                $(form_id).show().siblings().hide();
                event.preventDefault();
            });
            $('#back-to-login').click(self.do_exit);
            self.$el.find("td").addClass("oe_form_group_cell");
            self.$el.find("tr td:first-child").addClass("oe_form_group_cell_label");
            self.$el.find("label").addClass("oe_form_label");
            self.$el.find("form[name=create_db_form]").validate({ submitHandler: self.do_create });
            self.$el.find("form[name=duplicate_db_form]").validate({ submitHandler: self.do_duplicate });
            self.$el.find("form[name=drop_db_form]").validate({ submitHandler: self.do_drop });
            self.$el.find("form[name=backup_db_form]").validate({ submitHandler: self.do_backup });
            self.$el.find("form[name=restore_db_form]").validate({ submitHandler: self.do_restore });
            self.$el.find("form[name=change_pwd_form]").validate({
                messages: {
                    old_pwd: _t("Please enter your previous password"),
                    new_pwd: _t("Please enter your new password"),
                    confirm_pwd: {
                        required: _t("Please confirm your new password"),
                        equalTo: _t("The confirmation does not match the password")
                    }
                },
                submitHandler: self.do_change_password
            });
           this._super();
        },
    });
};
