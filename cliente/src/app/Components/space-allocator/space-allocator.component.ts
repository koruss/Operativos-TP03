import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { FileSystemService } from 'src/app/Services/file-system/file-system.service';

import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';

import FileSystem from 'src/app/Models/file-system';

@Component({
  selector: 'app-space-allocator',
  templateUrl: './space-allocator.component.html',
  styleUrls: ['./space-allocator.component.css']
})
export class SpaceAllocatorComponent implements OnInit {
  public fileSystem: FileSystem = {
    sector_size: 0,
    sector_amount: 0,
  };

  public sectorAmntControl: FormControl = new FormControl('', [
    Validators.required,
  ]);

  public sectorSizeControl: FormControl = new FormControl('', [
    Validators.required,
  ]);

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private dialog: MatDialog,
    private fileSystemService: FileSystemService
  ) { }

  ngOnInit(): void {
    console.log(this.fileSystemService.fsExists());
    // var exists = this.fileSystemService.fsExists();
  }

  public async onSubmitClick(): Promise<void> {
    try {
      // Validate input information
      if (
        !this.fileSystem.sector_size || 
        !this.fileSystem.sector_amount
      ) {
        this.snackBar.open('Información de tamaño inválida.', 'Close', {
          verticalPosition: 'top',
          duration: 3000,
        });
        return;
      }
      await this.fileSystemService.createFS({
        sector_size: this.fileSystem.sector_size,
        sector_amount: this.fileSystem.sector_amount
      });
      // Access drive
      this.snackBar.open('Filesystem creado exitosamente.', 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
      this.dialog.closeAll();
      this.router.navigateByUrl('/my-drive');
    } catch (err: any) {
      const { message } = err.error;
      this.snackBar.open(message, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
    }
  }

}
