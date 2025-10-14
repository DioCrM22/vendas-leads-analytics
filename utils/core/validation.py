import pandas as pd
from typing import Dict, Tuple, Any, List

class DataValidator:
    """Validador centralizado de estrutura de dados"""
    
    # Validações para dados de vendas
    VENDAS_VALIDATIONS = {
        "dados_mensais": {
            "required_columns": ["mes", "leads", "vendas", "receita", "conversao", "ticket_medio"],
            "numeric_columns": ["leads", "vendas", "receita", "conversao", "ticket_medio"],
            "description": "Dados mensais de performance",
            "primary_key": "mes",
            "expected_ranges": {
                "leads": (0, 100000),
                "vendas": (0, 10000),
                "receita": (0, 1000000),
                "conversao": (0, 1),
                "ticket_medio": (0, 10000)
            }
        },
        "dados_estados": {
            "required_columns": ["estado", "uf", "vendas", "lat", "lon", "regiao"],
            "numeric_columns": ["vendas", "lat", "lon"],
            "description": "Vendas por estado brasileiro",
            "primary_key": "uf",
            "expected_ranges": {
                "vendas": (0, 10000),
                "lat": (-35, 5),
                "lon": (-75, -30)
            }
        },
        "dados_marcas": {
            "required_columns": ["marca", "vendas", "categoria"],
            "numeric_columns": ["vendas"],
            "description": "Vendas por marca de veículo",
            "primary_key": "marca",
            "expected_ranges": {
                "vendas": (0, 10000)
            }
        },
        "dados_lojas": {
            "required_columns": ["loja", "vendas", "cidade", "estado"],
            "numeric_columns": ["vendas"],
            "description": "Performance por loja/concessionária",
            "primary_key": "loja",
            "expected_ranges": {
                "vendas": (0, 1000)
            }
        },
        "dados_visitas": {
            "required_columns": ["dia_semana", "visitas", "ordem"],
            "numeric_columns": ["visitas", "ordem"],
            "description": "Visitas por dia da semana",
            "primary_key": "dia_semana",
            "expected_ranges": {
                "visitas": (0, 10000),
                "ordem": (0, 6)
            }
        }
    }
    
    # Validações para dados de leads
    LEADS_VALIDATIONS = {
        "dados_genero": {
            "required_columns": ["genero", "leads"],
            "numeric_columns": ["leads"],
            "description": "Distribuição de leads por gênero",
            "primary_key": "genero",
            "expected_ranges": {
                "leads": (0, 100000)
            }
        },
        "dados_status_profissional": {
            "required_columns": ["status", "leads_percent"],
            "numeric_columns": ["leads_percent"],
            "description": "Status profissional dos leads",
            "primary_key": "status",
            "expected_ranges": {
                "leads_percent": (0, 100)
            }
        },
        "dados_faixa_etaria": {
            "required_columns": ["faixa", "leads_percent"],
            "numeric_columns": ["leads_percent"],
            "description": "Distribuição por faixa etária",
            "primary_key": "faixa",
            "expected_ranges": {
                "leads_percent": (0, 100)
            }
        },
        "dados_faixa_salarial": {
            "required_columns": ["faixa", "leads_percent", "ordem"],
            "numeric_columns": ["leads_percent", "ordem"],
            "description": "Distribuição por faixa salarial",
            "primary_key": "faixa",
            "expected_ranges": {
                "leads_percent": (0, 100),
                "ordem": (1, 10)
            }
        },
        "dados_classificacao_veiculo": {
            "required_columns": ["classificacao", "visitas"],
            "numeric_columns": ["visitas"],
            "description": "Visitas por classificação do veículo",
            "primary_key": "classificacao",
            "expected_ranges": {
                "visitas": (0, 100000)
            }
        },
        "dados_idade_veiculo": {
            "required_columns": ["idade", "visitas_percent", "ordem"],
            "numeric_columns": ["visitas_percent", "ordem"],
            "description": "Visitas por idade do veículo",
            "primary_key": "idade",
            "expected_ranges": {
                "visitas_percent": (0, 100),
                "ordem": (1, 10)
            }
        },
        "dados_veiculos_visitados": {
            "required_columns": ["marca", "modelo", "visitas"],
            "numeric_columns": ["visitas"],
            "description": "Veículos mais visitados",
            "primary_key": ["marca", "modelo"],
            "expected_ranges": {
                "visitas": (0, 10000)
            }
        }
    }
    
    @classmethod
    def get_validations(cls, domain: str = None) -> Dict[str, Any]:
        """Retorna validações por domínio"""
        if domain == 'vendas':
            return cls.VENDAS_VALIDATIONS
        elif domain == 'leads':
            return cls.LEADS_VALIDATIONS
        else:
            return {**cls.VENDAS_VALIDATIONS, **cls.LEADS_VALIDATIONS}
    
    @staticmethod
    def validate_column_addition(data_key: str, column_name: str, column_type: str) -> Tuple[bool, str]:
        """Valida adição de nova coluna"""
        if not column_name or not column_name.strip():
            return False, "Nome da coluna não pode estar vazio"
        
        if not column_name.replace('_', '').isalnum():
            return False, "Nome da coluna deve conter apenas letras, números e underscores"
        
        all_validations = DataValidator.get_validations()
        if data_key in all_validations:
            existing_columns = all_validations[data_key]["required_columns"]
            if column_name in existing_columns:
                return False, f"Coluna '{column_name}' já existe na tabela"
        
        return True, "Coluna válida"
    
    @staticmethod
    def get_validation_info(data_key: str) -> Dict[str, Any]:
        """Retorna informações de validação para uma tabela"""
        all_validations = DataValidator.get_validations()
        return all_validations.get(data_key, {})
    
    @staticmethod
    def validate_dataframe_structure(df: pd.DataFrame, data_key: str) -> Tuple[bool, str, pd.DataFrame]:
        """Valida estrutura completa do DataFrame"""
        all_validations = DataValidator.get_validations()
        
        if data_key not in all_validations:
            return True, "Validação não configurada para este dataset", df
        
        validation = all_validations[data_key]
        df_sanitized = df.copy()
        warnings = []
        
        # 1. Verificar colunas obrigatórias
        missing_columns = [col for col in validation["required_columns"] if col not in df.columns]
        if missing_columns:
            return False, f"❌ Colunas obrigatórias faltando: {', '.join(missing_columns)}", df_sanitized
        
        # 2. Sanitizar colunas numéricas
        for numeric_col in validation["numeric_columns"]:
            if numeric_col in df_sanitized.columns:
                original_non_null = df_sanitized[numeric_col].notna().sum()
                df_sanitized[numeric_col] = pd.to_numeric(df_sanitized[numeric_col], errors='coerce')
                new_non_null = df_sanitized[numeric_col].notna().sum()
                
                if new_non_null < original_non_null:
                    lost_values = original_non_null - new_non_null
                    warnings.append(f"⚠️ {lost_values} valor(es) não numérico(s) convertido(s) para NaN em '{numeric_col}'")
        
        # 3. Verificar duplicatas na chave primária
        primary_key = validation.get("primary_key")
        if primary_key:
            key_columns = primary_key if isinstance(primary_key, list) else [primary_key]
            
            if all(pk in df_sanitized.columns for pk in key_columns):
                duplicates = df_sanitized.duplicated(subset=key_columns, keep=False)
                if duplicates.any():
                    duplicate_count = duplicates.sum()
                    warnings.append(f"⚠️ {duplicate_count} registro(s) com chave duplicada")
        
        # 4. Validar ranges esperados
        expected_ranges = validation.get("expected_ranges", {})
        for col, (min_val, max_val) in expected_ranges.items():
            if col in df_sanitized.columns:
                out_of_range = ((df_sanitized[col] < min_val) | (df_sanitized[col] > max_val)) & df_sanitized[col].notna()
                if out_of_range.any():
                    out_of_range_count = out_of_range.sum()
                    warnings.append(f"⚠️ {out_of_range_count} valor(es) fora do range esperado ({min_val}-{max_val}) em '{col}'")
        
        # 5. Verificar valores nulos em colunas obrigatórias
        for req_col in validation["required_columns"]:
            if req_col in df_sanitized.columns:
                null_count = df_sanitized[req_col].isna().sum()
                if null_count > 0:
                    warnings.append(f"⚠️ {null_count} valor(es) nulo(s) em coluna obrigatória '{req_col}'")
        
        # Construir mensagem final
        if warnings:
            final_message = "✅ Estrutura válida com avisos:\n" + "\n".join(warnings)
        else:
            final_message = "✅ Dados validados com sucesso"
        
        return True, final_message, df_sanitized
    
    @staticmethod
    def highlight_problematic_rows(df: pd.DataFrame, data_key: str) -> pd.DataFrame:
        """Destaca linhas problemáticas no DataFrame"""
        all_validations = DataValidator.get_validations()
        
        if data_key not in all_validations:
            return df
        
        validation = all_validations[data_key]
        df_result = df.copy()
        
        # Inicializar colunas de problemas
        df_result['_problema_numerico'] = False
        df_result['_problema_obrigatorio'] = False
        df_result['_problema_range'] = False
        df_result['_problema_duplicata'] = False
        df_result['_problemas_detalhes'] = ""
        
        # 1. Verificar problemas numéricos
        for numeric_col in validation["numeric_columns"]:
            if numeric_col in df_result.columns:
                numeric_problems = pd.to_numeric(df_result[numeric_col], errors='coerce').isna() & df_result[numeric_col].notna()
                df_result.loc[numeric_problems, '_problema_numerico'] = True
                df_result.loc[numeric_problems, '_problemas_detalhes'] += f"{numeric_col} não numérico; "
        
        # 2. Verificar valores nulos em obrigatórios
        for req_col in validation["required_columns"]:
            if req_col in df_result.columns:
                null_problems = df_result[req_col].isna()
                df_result.loc[null_problems, '_problema_obrigatorio'] = True
                df_result.loc[null_problems, '_problemas_detalhes'] += f"{req_col} nulo; "
        
        # 3. Verificar ranges
        expected_ranges = validation.get("expected_ranges", {})
        for col, (min_val, max_val) in expected_ranges.items():
            if col in df_result.columns:
                range_problems = ((df_result[col] < min_val) | (df_result[col] > max_val)) & df_result[col].notna()
                df_result.loc[range_problems, '_problema_range'] = True
                df_result.loc[range_problems, '_problemas_detalhes'] += f"{col} fora do range; "
        
        # 4. Verificar duplicatas
        primary_key = validation.get("primary_key")
        if primary_key:
            key_columns = primary_key if isinstance(primary_key, list) else [primary_key]
            if all(pk in df_result.columns for pk in key_columns):
                duplicate_mask = df_result.duplicated(subset=key_columns, keep=False)
                df_result.loc[duplicate_mask, '_problema_duplicata'] = True
                df_result.loc[duplicate_mask, '_problemas_detalhes'] += "Chave duplicada; "
        
        # Limpar detalhes vazios
        df_result['_problemas_detalhes'] = df_result['_problemas_detalhes'].str.rstrip('; ')
        
        return df_result
    
    @staticmethod
    def get_table_description(data_key: str) -> str:
        """Retorna descrição da tabela"""
        all_validations = DataValidator.get_validations()
        return all_validations.get(data_key, {}).get("description", "Sem descrição disponível")
    
    @staticmethod
    def get_required_columns(data_key: str) -> List[str]:
        """Retorna colunas obrigatórias da tabela"""
        all_validations = DataValidator.get_validations()
        return all_validations.get(data_key, {}).get("required_columns", [])
    
    @staticmethod
    def get_numeric_columns(data_key: str) -> List[str]:
        """Retorna colunas numéricas da tabela"""
        all_validations = DataValidator.get_validations()
        return all_validations.get(data_key, {}).get("numeric_columns", [])