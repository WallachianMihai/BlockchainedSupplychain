package com.example.manufacturergui.model;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class Contract
{
    private Integer id;
    private String company;
    private String product;
    private Integer quantity;
    private String contractPath;

    public Contract(Integer id, String company, String product, Integer quantity, String contractPath)
    {
        this.id = id;
        this.company = company;
        this.product = product;
        this.quantity = quantity;
        this.contractPath = contractPath;
    }
}
