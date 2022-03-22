<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "meanings" %>

<h2>${_('Meaning')} ${ctx.id}</h2>

<%util:table items="${ctx.forms}" args="item" options="${dict(bInfo=True)}">
    <%def name="head()">
        <th>Form</th>
        <th>Language</th>
        <th>Contribution</th>
    </%def>
    <td>${h.link(request, item.form)}</td>
    <td>${h.link(request, item.form.language)}</td>
    <td>${h.link(request, item.form.contribution)}</td>
</%util:table>