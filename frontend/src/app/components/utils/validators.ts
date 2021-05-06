import { FormGroup } from '@angular/forms';
export function senhaValidator(
  form: FormGroup
): { [s: string]: boolean } | null {
  if (!form || !form.get('password') || !form.get('password2')) {
    return null;
  }

  return form.get('password')?.value === form.get('password2')?.value
    ? null
    : { notSame: true };
}
