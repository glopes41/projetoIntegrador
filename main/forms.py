from django import forms
from .models import Prova, Avaliacao, Tipo, Concurso


class FormAvaliacao(forms.ModelForm):
    tipo_prova = forms.ModelChoiceField(
        label='Tipo da Prova', queryset=Tipo.objects.all())

    class Meta:
        model = Avaliacao
        fields = ['nota', 'candidato', 'avaliacao']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Instancia concurso
        concurso = Concurso.objects.first()
        # Obtendo os dados do formulário
        tipo_prova_descricao = self.cleaned_data['tipo_prova']
        # Insere a data automaticamente
        instance.data = concurso.data
        # Verificando se a instância já tem uma prova associada
        if not instance.prova_id:
            # Criando a Prova apenas se não houver uma associada à Avaliação
            tipo_prova_obj = Tipo.objects.get(descricao=tipo_prova_descricao)
            nova_prova = Prova.objects.create(
                tipo=tipo_prova_obj, concurso=concurso)
            instance.prova = nova_prova

        if commit:
            instance.save()
            self.save_m2m()

        return instance.prova
