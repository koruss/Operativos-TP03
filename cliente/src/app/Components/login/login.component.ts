import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthenticationService } from '../../Services/authentication/authentication.service';

import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SignUpComponent } from '../sign-up/sign-up.component';

import User from '../../Models/user.model';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  public user: User = {
    username: '',
    password: '',
  };

  public loginFormControl: FormControl = new FormControl('', [
    Validators.required,
  ]);
  public passwordFormControl: FormControl = new FormControl('', [
    Validators.required,
  ]);

  constructor(
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private routerService: Router,
    private authenticationService: AuthenticationService
  ) {}

  ngOnInit(): void {}

  /**
   * Opens the signup dialog
   */
  public openDialog(): void {
    this.dialog.open(SignUpComponent);
  }

  /**
   * Authenticates user with entered credentials
   * @returns void
   */
  public async onSignInClick(): Promise<void> {
    try {
      await this.authenticationService.authenticateUser(this.user);
      // Store user profile information
      this.authenticationService.setIsAuthenticated(true);
      this.authenticationService.setUserInformation({
        username: this.user.username,
      });
      // Access drive
      this.snackBar.open(`Welcome ${this.user.username}`, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
      this.routerService.navigateByUrl('/my-drive');
    } catch (err: any) {
      const { message } = err.error;
      this.snackBar.open(message, 'Close', {
        verticalPosition: 'top',
        duration: 3000,
      });
    }
  }
}
