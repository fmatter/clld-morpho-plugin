<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%namespace name="mutil" file="../morphology_util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>
% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry 

<%! active_menu_item = "morphemes" %>


<%doc><h2>${_('Morpheme')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Morpheme')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Label:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        <tr>
            <td>Allomorphs:</td>
            <td>
                % for i, morph in enumerate(ctx.allomorphs):
                    % if i < len(ctx.allomorphs)-1:
                        <% comma = "," %>
                    % else:
                        <% comma = "" %>
                    % endif
                <i>${h.link(request, morph)}</i>${comma}
                % endfor
            </td>
        </tr>
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
        % if contribution in dir(ctx):
        <tr>
            <td> Contribution:</td>
            <td>
                ${h.link(request, ctx.contribution)} by
% for contributor in ctx.contribution.primary_contributors:
${h.link(request, contributor)}
% endfor
            </td>
        </tr>
        % endif
    </tbody>
</table>


% if len(ctx.meanings[0].morph_tokens) > 0:
    <% meaning_sentences = {} %>
    <h3>${_('Word forms')}</h3>
    % for meaning in ctx.meanings:
        <%meaning_sentences[meaning] = []%>
        % if meaning.morph_tokens:
            <h4> As ${h.link(request, meaning.meaning)}:</h4>
            <ol>
                % for s in meaning.morph_tokens:
                    <li>${h.link(request, s.form)}</li>
                    <%meaning_sentences[meaning].extend(s.form.sentence_assocs)%>
                % endfor
            </ol>
        % endif
    % endfor
    <h3>${_('Sentences')}</h3>
    % for morpheme_meaning, sentences in meaning_sentences.items():
        <div id=${morpheme_meaning.id}>
            <h4> As ${h.link(request, morpheme_meaning.meaning)}:</h4>
            <ol class="example">
                % for sentence in sentences:
                        ${rendered_sentence(request, sentence.sentence, sentence_link=True)}
                % endfor
            </ol>
        </div>
        <script>
            var highlight_div = document.getElementById("${morpheme_meaning.id}");
            var highlight_targets = highlight_div.querySelectorAll("*[name='${morpheme_meaning.id}']")
            for (index = 0; index < highlight_targets.length; index++) {
                highlight_targets[index].classList.add("morpho-highlight");
            }
        </script>
    % endfor
% endif
