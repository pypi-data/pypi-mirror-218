import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { MainAreaWidget, ICommandPalette } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { LabIcon } from '@jupyterlab/ui-components';
import { requestAPI } from './handler';
import { CounterWidget } from './widget';
import { connect } from './ws';

import IconSvg from '../style/svg/icon.svg';

import '../style/index.css';

/**
 * The command IDs used by the jupyter-operator plugin.
 */
namespace CommandIDs {
  export const create = 'create-jupyter-operator-widget';
}

/**
 * Initialization data for the @datalayer/jupyter-operator extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@datalayer/jupyter-operator:plugin',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [ISettingRegistry, ILauncher],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher
  ) => {
    const { commands } = app;
    const command = CommandIDs.create;
    const IconIcon = new LabIcon({
      name: 'jupyter-operator:icon',
      svgstr: IconSvg,
    });
    commands.addCommand(command, {
      caption: 'Show Jupyter Operator',
      label: 'Jupyter Operator',
      icon: (args: any) => IconIcon,
      execute: () => {
        const content = new CounterWidget();
        const widget = new MainAreaWidget<CounterWidget>({ content });
        widget.title.label = 'Jupyter Operator';
        widget.title.icon = IconIcon;
        app.shell.add(widget, 'main');
      }
    });
    const category = 'Datalayer';
    palette.addItem({ command, category });
    if (launcher) {
      launcher.add({
        command,
        category,
        rank: 2
      });
    }
    console.log('JupyterLab extension @datalayer/jupyter-operator is activated!');
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('@datalayer/jupyter-operator settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for @datalayer/jupyter-operator.', reason);
        });
    }
    connect('ws://localhost:8686/api/jupyter/jupyter_operator/echo', true);
    requestAPI<any>('get_config')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The Jupyter Server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
