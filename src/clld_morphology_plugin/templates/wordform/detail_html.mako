<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.util import rendered_form %>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>
% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry
<%! active_menu_item = "wordforms" %>



<h3>${_('Form')} <i>${ctx.name}</i> ‘${ctx.description}’</h3>

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
                ${rendered_form(request, ctx) | n}<br>
                ${rendered_form(request, ctx, level="gloss") | n}
            </td>
        </tr>
        % endif
        % if ctx.meanings:
        <tr>
            <td> Meanings:</td>
            <td>
                <ol>
                    % for meaning in ctx.meanings:
                        <li> ‘${h.link(request, meaning.meaning)}’ </li>
                    % endfor
                </ol>
            </td>
        </tr>
        % endif
        % if ctx.pos:
        <tr>
            <td>Part of speech:</td>
            <td>
                ${h.link(request, ctx.pos)}
            </td>
        </tr>
        % endif
        % if getattr(ctx, "segments", None):
            <tr>
                <td>Segments:</td>
                <td>
                % for segment in ctx.segments:
                ${h.link(request, segment.phoneme)}
                    % endfor</td>
            </tr>
        % endif
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        % if ctx.source:
            <tr>
                <td>Source:</td>
                <td>${h.link(request, ctx.source)}</td>
            </tr>
        % endif
    </tbody>
</table>

% if ctx.audio:
    <audio controls="controls"><source src="/audio/${ctx.audio}" type="audio/x-wav"></source></audio>
% endif 

<script>
var highlight_targets = document.getElementsByName("${ctx.id}");
for (index = 0; index < highlight_targets.length; index++) {
    highlight_targets[index].children[0].classList.add("morpho-highlight");
}
</script>