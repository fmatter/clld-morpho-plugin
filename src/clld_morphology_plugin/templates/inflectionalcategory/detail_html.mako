<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>

<%! active_menu_item = "inflectionalcategories" %>

<h3>${_('Inflectional category')} ${ctx.name}</h3>
Values:
<ul>
% for val in ctx.values:
    <li>${h.link(request, val)} (${val.name})</li>
% endfor
</ul>

${ctx.value_order}