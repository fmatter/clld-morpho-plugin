<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "units" %>


<%doc><h2>${_('Form')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Form')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Form:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        % if ctx.morphs:
        <tr>
            <td>Structure:</td>
            <td>
                    ${h.text2html("-".join([h.link(request, form.morph, label=string) for string, form in zip(ctx.name.split("-"), ctx.morphs)]))}
            </td>
        </tr>
        % endif
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
    </tbody>
</table>

