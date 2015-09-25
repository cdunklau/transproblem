from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.i18n import TranslationStringFactory
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request
from pkg_resources import resource_filename

import deform.widget

import colander


_ = TranslationStringFactory('tutorial')


class MailingSchema(colander.MappingSchema):
    email = colander.SchemaNode(
        colander.String(),
        validator=colander.Email(),
        title=_('Email Address'),
        widget=deform.widget.CheckedInputWidget(),
    )



def hello_world(request):
    print('Incoming request')
    form = deform.Form(
        MailingSchema(),
        buttons=(deform.Button('submit', title=_('Register')),),
    )
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            form.validate(controls)
        except deform.ValidationFailure as e:
            rendered_form = e.render()
        else:
            body = '<body><h1>{0}</h1></body>'.format(
                _('Registration Successful!'))
            return Response(body)
    else:
        rendered_form = form.render()
    body = '<body><h1>{0}</h1>{1}</body>'.format(
        _('Register for our mailing list'), rendered_form)
    return Response(body)


def locale(request):
    return Response(
        '<body><h1>Detected locale: {0}</h1></body>'.format(request.locale_name))


def main(global_config, **settings):
    config = Configurator()
    config.include('pyramid_debugtoolbar')

    config.registry.setdefault('default_locale_name', 'en')
    config.add_translation_dirs(
        'tutorial:locale/',
        'colander:locale',
        'deform:locale',
    )

    def translator(term):
        return get_localizer(get_current_request()).translate(term)

    deform_template_dir = resource_filename('deform', 'templates/')
    zpt_renderer = deform.ZPTRendererFactory(
        [deform_template_dir], translator=translator)
    deform.Form.set_default_renderer(zpt_renderer)

    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')
    config.add_route('locale', '/locale')
    config.add_view(locale, route_name='locale')
    config.add_static_view('static', 'static', cache_max_age=3600)

    return config.make_wsgi_app()
