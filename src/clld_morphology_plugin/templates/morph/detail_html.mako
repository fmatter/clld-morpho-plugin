<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>

% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry 
<%! active_menu_item = "morphs" %>


<%doc><h2>${_('Morph')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Morph')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Form:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        <tr>
            <td> Morpheme:</td>
            <td>${h.link(request, ctx.morpheme)}</td>
        </tr>
        <tr>
            <td> Meanings:</td>
            <td>
                <ol>
                    % for meaning in ctx.morpheme.meanings:
                        <li> ‘${h.link(request, meaning.meaning)}’ </li>
                    % endfor
                </ol>
            </td>
        </tr>
        % if cognates in dir(ctx):
        <tr>
            <td>Cognate set(s):</td>
            <td>
              <%
                cogsets = []
              %>
                    % for c in ctx.cognates:
                        % if c.cognateset not in cogsets:
                            <%
                                cogsets.append(c.cognateset)
                            %>
                        % endif
                    % endfor
                    ${h.text2html("*"+"+".join([h.link(request, c) for c in cogsets]))}
            </td>
            % for c in ctx.cognates:
                ${type(c.cognateset)}
            % endfor
        </tr>
        % endif
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

% if ctx.forms:
    <% meaning_sentences = {} %>
    <h3>${_('Word forms')}</h3>
    % for meaning in ctx.morpheme.meanings:
        <%meaning_sentences[meaning] = []%>
        % if meaning.morph_tokens:
            <h4> As ${h.link(request, meaning.meaning)}:</h4>
            <ol>
            % for s in meaning.morph_tokens:
                % if s.morph == ctx:
                    <li>
                        ${h.link(request, s.form)}
                    </li>
                    <%meaning_sentences[meaning].extend(s.form_meaning.form_tokens)%>
                %endif
            % endfor
        </ol>
    %endif
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

