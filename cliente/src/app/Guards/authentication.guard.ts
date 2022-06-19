import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthenticationService } from '../Services/authentication/authentication.service';

@Injectable()
export class AuthenticationGuard implements CanActivate {
  constructor(
    private authenticationService: AuthenticationService,
    private routerService: Router
  ) {}

  canActivate(): boolean {
    if (this.authenticationService.getIsAuthenticated()) {
      return true;
    }
    this.routerService.navigateByUrl('/');
    return false;
  }
}
