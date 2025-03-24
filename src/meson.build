pkgdatadir = join_paths(get_option('prefix'), get_option('libdir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'hyprland_settings')

gnome = import('gnome')

gresource = gnome.compile_resources(
  'hyprland-settings',
  'hyprland-settings.gresource.xml',
  gresource_bundle: true,
  source_dir: '.',
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'hyprland-settings.in',
  output: 'hyprland-settings',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

hyprland_settings_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'settings.py',
]

install_data(hyprland_settings_sources, install_dir: moduledir)
install_subdir('library', install_dir: moduledir)
install_subdir('modules', install_dir: moduledir)
install_subdir('json', install_dir: moduledir)
install_subdir('scripts', install_dir: moduledir)