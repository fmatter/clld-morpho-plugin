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

<h3>${_('Morpheme')} <i>${ctx.name}</i> ‘${ctx.description}’</h3>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        <tr>
            % if ctx.allomorphs:
                <td> Morphs: </td>
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
            %endif
        </tr>
        % if ctx.glosses:
            <tr>
                <td>Glosses:</td>
                <td>
                    ${h.text2html(", ".join([".".join([h.link(request, gloss.gloss) for gloss in glosslist]) for glosslist in ctx.glosses]))}
                </td>
            </tr>
        %endif
        ##% if ctx.stems:
        ##<tr>
        ##   <td> Corresponding stem: </td>
        ##    <td>
        ##        % for stem in ctx.stems:
        ##            ${h.link(request, stem, label=stem.name.upper())} <br>
        ##        % endfor
        ##    </td>
        ##</tr>
        ##% endif
        ##% if ctx.derived_lexemes:
        ##<tr>
        ##   <td> Derived lexemes: </td>
        ##    <td>
        ##        <ol>
        ##            % for lex in ctx.derived_lexemes:
        ##                <li> ${h.link(request, lex.lexeme, label=lex.lexeme.name.upper())} ‘${lex.lexeme.description}’ </li>
        ##            % endfor
        ##        </ol>
        ##    </td>
        ##</tr>
        ##% endif
        ##% if ctx.comment:
        ##   <td> Comment: </td>
        ##   <td> ${parent.markdown(request, ctx.comment)|n} </td>
        ##% endif
        ##% if contribution in dir(ctx):
        ##<tr>
        ##    <td> Contribution: </td>
        ##    <td>
        ##        ${h.link(request, ctx.contribution)} by
        ##        % for contributor in ctx.contribution.primary_contributors:
        ##            ${h.link(request, contributor)}
        ##        % endfor
        ##    </td>
        ##</tr>
        ##% endif
    </tbody>
</table>

<% meaning_forms = {} %>
<% meaning_sentences = {} %>
##% for morph in ctx.allomorphs:
##    % for form_slice in morph.forms:
##        % if not form_slice.morpheme_meaning:
##            <li> ${h.link(request, form_slice.form)} </li>
##        % else:
##            <% meaning_forms.setdefault(form_slice.morpheme_meaning, []) %>
##            <% meaning_forms[form_slice.morpheme_meaning].append(form_slice.form) %>
##            % if getattr(form_slice.form_meaning, "form_tokens", None):
##                <% meaning_sentences.setdefault(form_slice.morpheme_meaning, []) %>
##                <% meaning_sentences[form_slice.morpheme_meaning].extend(form_slice.form_meaning.form_tokens) %>
##            % endif
##        % endif
##    % endfor
##% endfor

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#corpus" data-toggle="tab"> Corpus tokens </a></li>
        <li><a href="#forms" data-toggle="tab"> Wordforms </a></li>
    </ul>

    <div class="tab-content" style="overflow: visible;">
        <div id="forms" class="tab-pane">
        <ol>
            % for form in ctx.forms:
                <li> ${h.link(request, form)} </li>
            % endfor
        </ol>
        </div>
    
        <div id="corpus" class="tab-pane active">
            % for morpheme_meaning, sentences in meaning_sentences.items():
                <div id=${morpheme_meaning.id}>
                    % if len(meaning_forms) > 1:
                        <h5> As ‘${h.link(request, morpheme_meaning.meaning)}’:</h5>
                    % endif
                    <button type="button" class="btn btn-link" onclick="copyIDs('${morpheme_meaning.id}-ids')">Copy sentence IDs</button>
                    <code class="id_list" id=${morpheme_meaning.id}-ids> ${" ".join([x.sentence.id for x in sentences])} </code>
                    <% stc_ids = [] %>
                    <ol class="example">
                        % for sentence in sentences:
                            % if sentence.sentence.id not in stc_ids:
                                ${rendered_sentence(request, sentence.sentence, sentence_link=True)}
                                <% stc_ids.append(sentence.sentence.id) %>
                            % endif
                        % endfor
                    </ol>
                </div>
                <script>
                    var highlight_div = document.getElementById("${morpheme_meaning.id}");
                    var highlight_targets = highlight_div.querySelectorAll("*[name*='${morpheme_meaning.id}']")
                    for (index = 0; index < highlight_targets.length; index++) {
                        highlight_targets[index].classList.add("morpho-highlight");
                    }
                </script>
            % endfor
        </div>
    </div>  
</div>

<script src="${req.static_url('clld_morphology_plugin:static/clld-morphology.js')}"></script>