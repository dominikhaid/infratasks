from pyinfra.operations import files, apt

from infratasks.utils.operations import Operation


class AppimagesOperation(Operation):
    name = "apps"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        apps = [
            "FontBase.AppImage",
            "webcatalog.AppImage",
            "App.Outlet.AppImage",
            "Nextcloud.AppImage",
            "firefox.AppImage",
            "Heynote.AppImage",
            "jetbrains-toolbox.tar.gz"]

        for app in apps:
            files.file(
                name="Remove {}".format(app),
                path="/home/dominik/Applications/{}".format(app),
                present=False,
            )

        files.directory(
            path="/home/dominik/Applications/",
            user="dominik",
            group="dominik",
        )

        files.download(
            name="Download FontBase",
            src="https://releases.fontba.se/linux/FontBase-2.16.4.AppImage",
            dest="/home/dominik/Applications/FontBase.AppImage",
            force=True
        )

        files.download(
            name="Download FontBase",
            src="https://github.com/heyman/heynote/releases/download/v1.7.0/Heynote_1.7.0_x86_64.AppImage",
            dest="/home/dominik/Applications/Heynote.AppImage",
            force=True
        )

        files.download(
            name="Download Webcatalog",
            src="https://github.com/webcatalog/webcatalog-app/releases/download/v35.1.1/webcatalog-35.1.1.AppImage",
            dest="/home/dominik/Applications/webcatalog.AppImage",
            force=True
        )

        files.download(
            name="Download App-Outlet",
            src="https://github.com/app-outlet/app-outlet/releases/download/v2.0.2/App.Outlet-2.0.2.AppImage",
            dest="/home/dominik/Applications/App.Outlet.AppImage",
            force=True
        )

        files.download(
            name="Download Nextcloud",
            src="https://github.com/nextcloud/desktop/releases/download/v3.2.4/Nextcloud-3.2.4-x86_64.AppImage",
            dest="/home/dominik/Applications/Nextcloud.AppImage",
            force=True
        )

        files.download(
            name="Download Firefox",
            src="https://github.com/srevinsaju/Firefox-Appimage/releases/download/firefox-v90.0.r20210721174149/firefox-90.0.r20210721174149-x86_64.AppImage",
            dest="/home/dominik/Applications/firefox.AppImage",
            force=True
        )

        files.download(
            name="Download Intelj Tools",
            src="https://download.jetbrains.com/toolbox/jetbrains-toolbox-2.0.4.17212.tar.gz",
            dest="/home/dominik/Applications/ideatoolbox.tar.gz",
            force=True
        )

        apt.deb(
            name="Installing AppImage Launcher",
            src="https://github.com/TheAssassin/AppImageLauncher/releases/download/v2.2.0/appimagelauncher_2.2.0-travis995.0f91801.bionic_amd64.deb",
            _sudo=True
        )

    def delete_debian_amd64(self):
        pass
        # TODO VERSIONS TO VARIABLES CHECK IF EXISTING
