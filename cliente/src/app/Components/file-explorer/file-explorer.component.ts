import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DirectoryService } from '../../Services/directory/directory.service';
import { DriveService } from '../../Services/drive/drive.service';
import { FileService } from '../../Services/file/file.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { FileViewComponent } from '../file-view/file-view.component';
import { CreateDirectoryComponent } from '../create-directory/create-directory.component';
import { CreateFileComponent } from '../create-file/create-file.component';
import { UploadFileComponent } from '../upload-file/upload-file.component';
import { saveAs } from 'file-saver';

import Drive from '../../Models/drive.model';
import Directory from '../../Models/directory.model';
import File from '../../Models/file.model';
import { MoveComponent } from '../move/move.component';

@Component({
  selector: 'app-file-explorer',
  templateUrl: './file-explorer.component.html',
  styleUrls: ['./file-explorer.component.css']
})
export class FileExplorerComponent implements OnInit {
  path: string[] = [];
  files: File[] = [];
  directories: Directory[] = [];
  directory: Drive = {};
  users: string[] = [];

  spacePercentage: number = 0;

  currentDirectory: string = '';
  directoryClicks: number = 0;

  constructor(
    private dialog: MatDialog,
    private routerService: Router,
    private dirService: DirectoryService,
    private driveService: DriveService,
    private fileService: FileService,
    private snackBar: MatSnackBar
  ) { }

  async ngOnInit(): Promise<void> {
      await this.getDir('root/');
      this.path.push('root');
      this.driveService.appendDirectoryToPath('root');
      //await this.getSpace(this.user.username);
  }
  /**
   *
   * @returns used percentage
   */
  public getPercentageValue(usedSpace: any, totalSpace: any) {
    let percenatage = (usedSpace * 100) / totalSpace;

    return percenatage;
  }

  public getCurrentPath() {
    var tmp_path = '';
    this.path.forEach((segment) => {
      tmp_path = tmp_path.concat(segment + '/');
    });
    console.log(tmp_path)
    return tmp_path;
  }

  /**
   * Opens the fileView Dialog
   */
  public async openDialog(file: File): Promise<void> {
    let dialogRef = this.dialog.open(FileViewComponent);
    dialogRef.componentInstance.file = file;
    dialogRef.componentInstance.path = this.path;
  }

  /**
   * Gets selected file
   * @returns void
   */
  public async getFile(filename: any) {
    let file = await this.fileService.getFile(this.getCurrentPath(), filename);
    this.openDialog(file);
  }

  /**
   * Download file
   * @returns void
   */
  public async downloadFile(filename: any) {
    let file: File = await this.fileService.getFile(
      this.getCurrentPath(),
      filename
    );
    if (file.content != undefined) {
      let blob = new Blob([file.content], { type: 'text/plain;charset=utf-8' });
      saveAs(blob, file.name);
    }
  }

  /**
   * Deletes selected file
   * @returns void
   */
  public async removeFile(filename: any) {
    try {
      let file = { filePath: this.getCurrentPath(), fileName: filename };
      await this.fileService.deleteFile(file);
      this.snackBar.open('File deleted successfully', 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
      await this.getDir(this.getCurrentPath());
    } catch (err: any) {
      console.log(err.error);
      const { message } = err.error;
      this.snackBar.open(message, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
    }
  }

  /**
   * Opens the dialog for creating a new file
   */
  public openCreateFileDialog(): void {
    const createFileDialog: MatDialogRef<CreateFileComponent> =
      this.dialog.open(CreateFileComponent, {
        width: '600px',
      });
    createFileDialog
      .afterClosed()
      .subscribe(async (shouldDirectoriesGetRefreshed: boolean) => {
        if (shouldDirectoriesGetRefreshed) {
          await this.getDir(this.getCurrentPath());
        }
      });
  }

  /**
   * Opens the dialog for uploading a new file
   */
  public openUploadFileDialog(): void {
    const createUploadFileDialog: MatDialogRef<UploadFileComponent> =
      this.dialog.open(UploadFileComponent, {
        width: '600px',
      });
    createUploadFileDialog
      .afterClosed()
      .subscribe(async (shouldDirectoriesGetRefreshed: boolean) => {
        if (shouldDirectoriesGetRefreshed) {
          await this.getDir(this.getCurrentPath());
        }
      });
  }

  /**
   * Opens Move Dialog
   * @returns void
   */
  public async openMoveDialog(filename: any, type: boolean) {
    let dialogRef = this.dialog.open(MoveComponent);
    dialogRef.componentInstance.type = type;
    dialogRef.componentInstance.move = true;
    dialogRef.componentInstance.file = filename;
    dialogRef.componentInstance.filePath = this.getCurrentPath();

    dialogRef.afterClosed().subscribe(async () => {
      await this.getDir(this.getCurrentPath());
    });
  }

  /**
   * Opens Copy Dialog
   * @returns void
   */
  public async openCopyDialog(filename: any, type: boolean) {
    let dialogRef = this.dialog.open(MoveComponent);
    dialogRef.componentInstance.type = type;
    dialogRef.componentInstance.move = false;
    dialogRef.componentInstance.file = filename;
    dialogRef.componentInstance.filePath = this.getCurrentPath();

    dialogRef.afterClosed().subscribe(async () => {
      await this.getDir(this.getCurrentPath());
    });
  }

  /**
   * Change Dir to selected Dir
   * @returns void
   */
  public async onClickChangeDirForward(path: any) {
    if (path === this.currentDirectory && this.directoryClicks === 1) {
      this.path.push(path);
      this.driveService.appendDirectoryToPath(path);
      await this.getDir(this.getCurrentPath() + path);

      this.currentDirectory = '';
      this.directoryClicks = 0;
    } else {
      if (path !== this.currentDirectory) {
        this.directoryClicks = 1;
        this.currentDirectory = path;
      } else {
        this.directoryClicks++;
      }
    }
  }

  /**
   * Change Dir to selected Dir
   * @returns void
   */
  public async onClickChangeDirBackward(path: any) {
    let index = this.path.indexOf(path);
    this.path = this.path.slice(0, index + 1);
    this.driveService.setCurrentPath(
      this.driveService.getCurrentPath().slice(0, index + 1)
    );
    await this.getDir(this.getCurrentPath());
  }

  /**
   * Change Dir to selected Dir
   * @returns void
   */
  public async onClickChangeDir(path: any) {
    this.path = [];
    this.path.push(path);
    await this.getDir(this.getCurrentPath());
  }

  /**
   * Get dir from specific path
   * @returns void
   */
  public async getDir(path: string): Promise<void> {
    try {
      this.directory = await this.dirService.getDir(path);
      this.directories = this.directory.directories as Directory[];
      this.files = this.directory.files as File[];
    } catch (err: any) {
      const { message } = err.error;
      this.snackBar.open(message, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
    }
  }

  /**
   * Opens the dialog for creating a new directory
   */
  public openCreateDirectoryDialog(): void {
    const createDirectoryDialog: MatDialogRef<CreateDirectoryComponent> =
      this.dialog.open(CreateDirectoryComponent, {
        width: '500px',
      });
    createDirectoryDialog
      .afterClosed()
      .subscribe(async (shouldDirectoriesGetRefreshed: boolean) => {
        if (shouldDirectoriesGetRefreshed) {
          await this.getDir(this.getCurrentPath());
        }
      });
  }

  /**
   * Deletes selected direcotry
   * @returns void
   */
  public async removeDirectory(dirName: any) {
    try {
      let dir = { dirPath: this.getCurrentPath(), dirName: dirName };
      await this.dirService.deleteDir(dir);
      this.snackBar.open('Directory deleted successfully', 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });

      await this.getDir(this.getCurrentPath());
    } catch (err: any) {
      console.log(err.error);
      const { message } = err.error;
      this.snackBar.open(message, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
    }
  }

}
